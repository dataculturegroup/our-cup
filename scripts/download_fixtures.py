import requests
import json
import os
from dateutil.parser import parse
import logging

from worldcup.match_picker import FIXTURES_JSON_FILE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORLD_CUP_JSON_MATCH_URL = "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json"

logger.info("Starting to fetch games...")
data = requests.get(WORLD_CUP_JSON_MATCH_URL).json()
game_data = []
logger.info("  fetched JSON file from {}".format(WORLD_CUP_JSON_MATCH_URL))

logger.info("Loading matches...")
for round_info in data['rounds']:
    for match in round_info['matches']:
        match_date = parse(match['date'])
        match_info = {
            'date': str(match_date.year)+'/'+str(match_date.month)+'/'+str(match_date.day),
            'team1': match['team1']['code'],
            'team2': match['team2']['code']
        }
        game_data.append(match_info)

logger.debug("  found {} matches".format(len(game_data)))

logger.info("Writing output JSON...")
with open(FIXTURES_JSON_FILE, 'w') as outfile:
    json.dump(game_data, outfile)
logger.info("  write it to {}".format(FIXTURES_JSON_FILE))
