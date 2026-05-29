import json
import os
import re
import requests
from typing import Tuple
from dotenv import load_dotenv
from atproto import Client, Session, SessionEvent, client_utils
from atproto.exceptions import AtProtocolError
from atproto_client.exceptions import RequestException

import recommender


# CONSTANTS
load_dotenv()  # DEV: take environment variables from a local .env file

# the handle and password you want to check for mentions and reply from
BSKY_HANDLE   = os.environ["BSKY_HANDLE"]        # e.g. yourbot.bsky.social
BSKY_PASSWORD = os.environ["BSKY_APP_PASSWORD"]   # App Password from Bluesky settings

# GH -> Settings -> Developer Settings -> Personal Access Tokens -> Generate new token (select "gist" scope)
GITHUB_TOKEN  = os.environ["GH_TOKEN"]  # this will let us access the Gist

# Set up a GitHub Gist to store our state across runs. It holds two files: one for the cursor of the
# last processed notification (put "0" in it to start), and one for the Bluesky session string so we
# can resume an existing session instead of logging in fresh every run.
GIST_ID                = os.environ["GIST_ID"]  # Copy and paste from te URL of your Gist
GIST_CURSOR_FILENAME   = "wc26-bot-cursor.txt"   # don't need to hide these, so not in env-vars
GIST_SESSION_FILENAME  = "wc26-bot-session.txt"

ZIPCODE_RE = re.compile(r"\b(\d{5})\b")
URL_RE = re.compile(r"https?://[^\s]+")


def build_rich_text(text: str) -> client_utils.TextBuilder:
    """Bluesky won't auto-detect URLs — wrap the plain reply text in a TextBuilder so
    send_post emits proper byte-offset link facets."""
    tb = client_utils.TextBuilder()
    cursor = 0
    for match in URL_RE.finditer(text):
        if match.start() > cursor:
            tb.text(text[cursor:match.start()])
        url = match.group()
        # Per https://docs.bsky.app/docs/advanced-guides/post-richtext, strip trailing
        # .,;!? and a closing ) when the URL has no matching ( — otherwise the link
        # target includes the surrounding sentence punctuation.
        while url:
            if url[-1] in ".,;!?":
                url = url[:-1]
            elif url[-1] == ")" and "(" not in url:
                url = url[:-1]
            else:
                break
        tb.link(url, url)
        cursor = match.start() + len(url)
    if cursor < len(text):
        tb.text(text[cursor:])
    return tb


# State Helpers
# We use a GitHub Gist to store state across runs: the cursor of the last processed notification (so we
# don't reply twice to the same mention, even if the bot restarts) and the Bluesky session string (so we
# resume an existing session instead of creating a new one — Bluesky rate-limits us to ~10 new sessions
# per day).

def load_state() -> Tuple[str | None, str | None]:
    """Fetch the gist once and return (cursor, session_string). Either may be None if not stored yet."""
    resp = requests.get(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        timeout=10,
    )
    resp.raise_for_status()
    files = resp.json()["files"]

    cursor = files.get(GIST_CURSOR_FILENAME, {}).get("content", "").strip()
    cursor = cursor if cursor and cursor != "0" else None

    session = files.get(GIST_SESSION_FILENAME, {}).get("content", "").strip()
    session = session if session and session != "0" else None

    return cursor, session


def save_state(*, cursor: str | None = None, session: str | None = None) -> None:
    """Patch the gist with whichever pieces of state are provided. Only the files we pass get touched,
    so saving a refreshed session doesn't clobber the cursor and vice-versa."""
    files = {}
    if cursor is not None:
        files[GIST_CURSOR_FILENAME] = {"content": cursor}
    if session is not None:
        files[GIST_SESSION_FILENAME] = {"content": session}
    if not files:
        return
    requests.patch(
        f"https://api.github.com/gists/{GIST_ID}",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        json={"files": files},
        timeout=10,
    ).raise_for_status()


# Bot Logic
# Handle the found zipcode and return a reply text. In this case, it looks up pre-processed recommendations
# for which upcoming World Cup matches to watch in that area based on foreign born population data from the
# census.

def extract_zipcode(text: str) -> str | None:
    match = ZIPCODE_RE.search(text)
    return match.group(1) if match else None


def fetch_new_notifications(authenticated_client: Client, last_indexed_at: str | None) -> Tuple[list, str]:
    resp = authenticated_client.app.bsky.notification.list_notifications({"limit": 25})
    notifs = resp.notifications
    if not notifs:
        return []
    if last_indexed_at:
        new_notifs = [n for n in notifs if n.indexed_at > last_indexed_at]
    else:
        new_notifs = notifs
    mentions = [n for n in new_notifs if n.reason == "mention"]
    newest_indexed_at = max(n.indexed_at for n in notifs)
    return mentions, newest_indexed_at


# Execution
# Set up to run as a script every 5 minutes (fastest we can run on GH Actions).

def get_client(session_string: str | None) -> Client:
    """Resume the saved Bluesky session if we have one, otherwise log in fresh. We register a
    session-change callback so any session that gets created or refreshed is written back to the gist,
    keeping us under Bluesky's ~10-new-sessions-per-day rate limit."""
    client = Client()  # this handles speaking ATProto to and from Bluesky

    @client.on_session_change
    def persist_session(event: SessionEvent, session: Session) -> None:
        if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
            save_state(session=session.export())

    if session_string:
        try:
            client.login(session_string=session_string)  # resume the existing session
            return client
        except AtProtocolError as e:
            print(f"Saved session invalid ({e}); creating a new one.")

    client.login(BSKY_HANDLE, BSKY_PASSWORD)  # the callback above persists the new session
    return client


def run():
    recommender.load() # one time load of static data for fast lookups in the bot logic

    # We store the indexed_at of the most recently processed notification in the gist, alongside the
    # Bluesky session string. The atproto listNotifications `cursor` is a pagination marker (goes older),
    # not a "since" marker, so we can't use it for this — we fetch the latest batch and filter
    # client-side by indexed_at instead.
    last_indexed_at, session_string = load_state()

    client = get_client(session_string)

    mentions, newest_indexed_at = fetch_new_notifications(client, last_indexed_at)
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
                text=build_rich_text(reply_text),
                reply_to={"root": root_ref, "parent": parent_ref},
            )
        except RequestException as e:
            if e.response.status_code == 429:
                reset_ts = int(e.response.headers.get("ratelimit-reset", 0))
                reset_time = datetime.datetime.fromtimestamp(reset_ts)
                print(f"Rate limited. Resets at {reset_time}. Skipping.")
            else:
                raise
        except AtProtocolError as e:
            print(f"  ERROR posting reply: {e}")

    # Persist the newest indexed_at across the whole fetched batch (not just mentions) so we don't
    # re-scan notifications we've already considered, and mark them read server-side too.
    save_state(cursor=newest_indexed_at)
    client.app.bsky.notification.update_seen({"seen_at": newest_indexed_at})
    print("Done.")


if __name__ == "__main__":
    run()
