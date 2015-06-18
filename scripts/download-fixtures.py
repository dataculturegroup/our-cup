import requests, sys, json, os, logging
from dateutil.parser import parse

WORLD_CUP_JSON_MATCH_URL = "http://localhost:3000/matches/"

print("Starting to fetch games:")
all_games = requests.get(WORLD_CUP_JSON_MATCH_URL).json()
game_data = []

for game in all_games:
    game_date = parse(game['datetime'])
    if 'code' not in game['home_team']:
        continue
    game_data.append({
        'date': str(game_date.year)+'/'+str(game_date.month)+'/'+str(game_date.day),
        'team1': game['home_team']['code'],
        'team2': game['away_team']['code'],
        'previewURL':""
    })

with open(os.path.join('../','worldcup','data','world_cup_2015_games.json'), 'w') as outfile:
    json.dump(game_data, outfile)

print("Done")
