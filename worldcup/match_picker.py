import copy
import datetime
import json
import logging
import os
from operator import itemgetter

from worldcup import basedir
from worldcup.country_codes import CountryCodes

FIXTURES_JSON_FILE = os.path.join(basedir, 'worldcup', 'data', 'word_cup_2018_matches.json')

logger = logging.getLogger(__name__)


class MatchPicker(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._json_file_path = FIXTURES_JSON_FILE
        self._fixtures = json.load(open(self._json_file_path))
        self._logger.info("loaded from "+self._json_file_path)
        self._translator = CountryCodes()

    def by_population(self, country_pop_data):
        all_games = copy.deepcopy(self._fixtures)
        # country_alpha3_to_pop_map['USA'] = 1  # change the score so US doesn't show up very much, commented out because USA isn't in it!
        country_alpha3_to_pop_map = {m['country']:m['population'] for m in country_pop_data}
        for game in all_games:
            logger.debug("{} vs. {}".format(game['team1'], game['team2']))
            try:
                team1_pop = country_alpha3_to_pop_map[self._translator.getByFifaCode(game['team1']).iso]
            except KeyError:
                logger.warning("Can't find population data for {}".format(game['team1']))
                team1_pop = 0  # the country isn't our list of
            try:
                team2_pop = country_alpha3_to_pop_map[self._translator.getByFifaCode(game['team2']).iso]
            except KeyError:
                logger.warning("Can't find population data for {}".format(game['team2']))
                team2_pop = 0  # the country isn't our list of
            game['score'] = team1_pop + team2_pop

        prioritized_games = sorted(all_games, key=itemgetter('score'), reverse=True)
        for game in prioritized_games:
            game['team1Country'] = self._translator.getByFifaCode(game['team1'])
            game['team2Country'] = self._translator.getByFifaCode(game['team2'])
            game['date'] = datetime.datetime.strptime(game['date'], '%Y/%m/%d')
        return prioritized_games

    def participating_fifa_country_codes(self):
        team1_codes = set([game['team1'] for game in self._fixtures])
        team2_codes = set([game['team2'] for game in self._fixtures])
        combined = team1_codes.union(team2_codes)
        return combined