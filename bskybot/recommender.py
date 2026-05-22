import json
import os
import random
from typing import Dict
import datetime as dt
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus


# Static Data Helpers
# The data to support this is generated via scripts and all pre-computed, so the code here is just super fast table
# lookups and formatting.

zip_2_county = {}
zip_2_timezone = {}
fips_2_recs = {}
fixtures = {}
teams = {}

BLUESKY_MAX_CHARS = 300

DATA_DIR = "data"

RANDOM_INFO_KEYS = ['foodSearch', 'wikipediaUrl', 'globalVoicesUrl', 'spotify']

def load():
    # Call once to initialize from data
    global zip_2_county, zip_2_timezone, fips_2_recs, fixtures, teams
    # lookup from zip to county (for larger data pool so recs are better)
    with open(os.path.join(DATA_DIR, "zip-2-county.json"), "r") as f:
        zip_2_county = json.load(f)
        for entry in zip_2_county.values():
            entry['city'] = entry['city'].title()
    # lookup from zip to timezone (so we can localize the game times)
    with open(os.path.join(DATA_DIR, "zip-2-timezone.json"), "r") as f:
        zip_2_timezone = json.load(f)
    # pre-computed recommendations data
    with open(os.path.join(DATA_DIR, "county-recs.json"), "r") as f:
        fips_2_recs = json.load(f)
    # load the game list
    with open(os.path.join(DATA_DIR, "fixtures.json"), "r") as f:
        fixtures = json.load(f)
        for f in fixtures:
            gmt_datetime = dt.datetime.strptime(f['Date'], "%d/%m/%Y %H:%M").replace(tzinfo=dt.timezone.utc)
            f['gmt_datetime'] = gmt_datetime
    # load the info about teams
    with open(os.path.join(DATA_DIR, "teams.json"), "r") as f:
        teams = json.load(f)


def _as_local_time(zipcode: str, game_time_utc: dt.datetime) -> dt.datetime:
    # helper to convert the game time from UTC to local time in the recommended location for formatting the reply text
    timezone_name = zip_2_timezone.get(zipcode)
    if not timezone_name:
        return game_time_utc # reasonable fallback?
    local_dt = game_time_utc.astimezone(ZoneInfo(timezone_name)) # go from zip to timezone and localize
    return local_dt


def _random_info(team: Dict, zipcode: str) -> str:
    info_key = random.choice(RANDOM_INFO_KEYS)
    info_value = team.get(info_key)
    msg = ""
    if info_key == "foodSearch":
        if info_value is None:
            info_key = 'demonym'
            info_value = team.get(info_key)
        yelp_url = f"https://www.yelp.com/search?find_desc={quote_plus(info_value)}&find_loc={zipcode}"
        msg = f"Find local {info_value} food: {yelp_url}"
    elif info_key == "wikipediaUrl":
        if info_value is not None:
            msg = f"Learn about {team['name']}: {info_value}"
    elif info_key == "globalVoicesUrl":
        if info_value is not None:
            msg = f"Read local {team['demonym']} news: {info_value}"
    elif info_key == "spotify":
        if info_value is not None:
            playlist = random.choice(info_value)
            msg = f"Hear some {playlist['name']}: {playlist['url']}"
    return msg  # failsafe for missing data


def process_zipcode(zipcode: str) -> str:
    county = zip_2_county.get(zipcode)
    #print(f"Processing zipcode {zipcode}, found county: {county}")
    # handle invalid zip code
    if not county:
        return f"⚠️ Sorry, I couldn't find any data for zipcode {zipcode}. Is that a real US zipcode? 🤔"
    country_recs = fips_2_recs.get(county['county_fips'])  # a list of strs with country names
    country_teams = [teams.get(country_code) for country_code in country_recs]
    # handle not enough data to recommend
    if not country_recs:
        return f"⚠️ Sorry, I couldn't find any game recommendations for (zipcode {zipcode}). Prob not enough Census data to work with in {county['city']}, {county['state']} 😢"
    # assemble a real recommendation
    rec_text = ""
    # add in the flags for any countries
    flags = []
    for team_info in country_teams:
        if team_info and team_info.get('flag'):
            flags.append(team_info['flag'])
    rec_text += f"Fans in {zipcode} ({county['city']}, {county['state']}) are cheering for {', '.join(flags)} ⚽️🎉\n"
    # add in the next 3 relevant games
    game_recs = [ g for g in fixtures if (g['Home Team'] in country_recs) or (g['Away Team'] in country_recs)]
    if len(game_recs) == 1:
        rec_text += "Game to watch: "
    elif len(game_recs) > 1:
        rec_text += "Games to watch:\n"
    for game in game_recs[:3]:  # keep it short
        local_date = _as_local_time(zipcode, game['gmt_datetime'])
        rec_text += f"  {local_date.strftime('%b %d')}: {game['Home Team']} vs {game['Away Team']} @ {local_date.strftime('%-I%p')}\n"
    # random tidbit
    random_link = _random_info(country_teams[0], zipcode)
    # Bluesky caps posts at 300 graphemes. Only append the random_link if the base
    # rec_text fits, and only keep it appended if the combined text also fits.
    if len(rec_text) <= BLUESKY_MAX_CHARS:
        with_link = rec_text + random_link
        if len(with_link) <= BLUESKY_MAX_CHARS:
            rec_text = with_link
    # and return the text
    return rec_text
