import requests, sys, json, os, logging

MATCH_DAYS = 20
FOOTBALL_DB_BASE_URL = "http://footballdb.herokuapp.com/api/v1/event/world.2014/round/"

all_games = []

print("Starting to fetch games:")

for day in range(1,MATCH_DAYS):
    print("  round "+str(day))
    url = FOOTBALL_DB_BASE_URL+str(day)
    r = requests.get(url)
    info = r.json()
    for game in info['games']:
        all_games.append({
            'date': game['play_at'],
            'team1': game['team1_code'],
            'team2': game['team2_code'],
        })

with open(os.path.join('../','app','static','data','world_cup_2014_games.json'), 'w') as outfile:
    json.dump(all_games, outfile)

print("Done")
