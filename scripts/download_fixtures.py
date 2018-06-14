import requests
import json
import os
from dateutil.parser import parse
import logging

logging.basicConfig(level=logging.DEBUG)

WORLD_CUP_JSON_MATCH_URL = "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json"

logging.info("Starting to fetch games:")
data = requests.get(WORLD_CUP_JSON_MATCH_URL).json()
game_data = []

for round_info in data['rounds']:
    for match in round_info['matches']:
        game_date = parse(match['date'])
    game_data.append({
        'date': str(game_date.year)+'/'+str(game_date.month)+'/'+str(game_date.day),
        'team1': match['team1']['code'],
        'team2': match['team2']['code']
    })

with open(os.path.join('worldcup', 'data', 'world_cup_2018_matches.json'), 'w') as outfile:
    json.dump(game_data, outfile)

logging.info("Done")
