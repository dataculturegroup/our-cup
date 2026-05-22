import json
import os
import re
import requests
from dotenv import load_dotenv
from atproto import Client
from atproto.exceptions import AtProtocolError

import recommender


# CONSTANTS
load_dotenv()  # DEV: take environment variables from a local .env file

# the handle and password you want to check for mentions and reply from
BSKY_HANDLE   = os.environ["BSKY_HANDLE"]        # e.g. yourbot.bsky.social
BSKY_PASSWORD = os.environ["BSKY_APP_PASSWORD"]   # App Password from Bluesky settings

# GH -> Settings -> Developer Settings -> Personal Access Tokens -> Generate new token (select "gist" scope)
GITHUB_TOKEN  = os.environ["GH_TOKEN"]  # this will let us access the Gist

# Set up a GitHub Gist with a single file (named as GIST_FILENAME below) to store the cursor for the 
# last processed notification. Put "0" in the file to start.
GIST_ID       = os.environ["GIST_ID"]  # Copy and paste from te URL of your Gist
GIST_FILENAME = "wc26-bot-cursor.txt"  # don't need to hide this, so not in an env-var

ZIPCODE_RE = re.compile(r"\b(\d{5})\b")


# State Helpers
# We use a GitHub Gist to store the cursor indicated the last processed notification. This ensures that we
# don't reply twice to the same mention, even if the bot restarts.

def read_cursor() -> str | None:
    resp = requests.get(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        timeout=10,
    )
    resp.raise_for_status()
    content = resp.json()["files"][GIST_FILENAME]["content"].strip()
    return content if content and content != "0" else None


def write_cursor(cursor: str) -> None:
    requests.patch(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        json={"files": {GIST_FILENAME: {"content": cursor}}},
        timeout=10,
    ).raise_for_status()


# Bot Logic
# Handle the found zipcode and return a reply text. In this case, it looks up pre-processed recommendations
# for which upcoming World Cup matches to watch in that area based on foreign born population data from the
# census.

def extract_zipcode(text: str) -> str | None:
    match = ZIPCODE_RE.search(text)
    return match.group(1) if match else None


# Execution
# Set up to run as a script every 5 minutes (fastest we can run on GH Actions).

def run():
    recommender.load() # one time load of static data for fast lookups in the bot logic

    client = Client()  # this handles speaking ATProto to and from Bluesky
    client.login(BSKY_HANDLE, BSKY_PASSWORD)

    # We store the indexed_at of the most recently processed notification in the gist.
    # The atproto listNotifications `cursor` is a pagination marker (goes older), not a "since" marker,
    # so we can't use it for this — we fetch the latest batch and filter client-side by indexed_at instead.
    last_indexed_at = read_cursor()

    resp = client.app.bsky.notification.list_notifications({"limit": 25})
    notifs = resp.notifications

    if not notifs:
        print("No new notifications.")
        return

    if last_indexed_at:
        new_notifs = [n for n in notifs if n.indexed_at > last_indexed_at]
    else:
        new_notifs = notifs

    mentions = [n for n in new_notifs if n.reason == "mention"]

    print(f"Found {len(mentions)} unread mention(s).")

    for notif in mentions:
        post = notif.record
        text = getattr(post, "text", "") or ""
        zipcode = extract_zipcode(text)

        if not zipcode:
            print(f"  Skipping mention from @{notif.author.handle} — no zipcode found.")
            continue

        reply_text = recommender.process_zipcode(zipcode)
        print(f"  Replying to @{notif.author.handle} for zip {zipcode}.")

        try:
            parent_ref = {
                "uri": notif.uri,
                "cid": notif.cid,
            }
            # Root is the top of the thread; if the mention is itself a reply, walk up.
            # For simplicity we treat the mention as both root and parent here.
            root_ref = parent_ref

            if hasattr(post, "reply") and post.reply:
                root_ref = {
                    "uri": post.reply.root.uri,
                    "cid": post.reply.root.cid,
                }

            client.send_post(
                text=reply_text,
                reply_to={"root": root_ref, "parent": parent_ref},
            )
        except AtProtocolError as e:
            print(f"  ERROR posting reply: {e}")

    # Persist the newest indexed_at across the whole fetched batch (not just mentions) so we don't
    # re-scan notifications we've already considered, and mark them read server-side too.
    newest_indexed_at = max(n.indexed_at for n in notifs)
    write_cursor(newest_indexed_at)
    client.app.bsky.notification.update_seen({"seen_at": newest_indexed_at})
    print("Done.")


if __name__ == "__main__":
    run()
