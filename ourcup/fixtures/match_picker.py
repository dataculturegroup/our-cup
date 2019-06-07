import copy
import datetime
import json
import logging
import os
from operator import itemgetter

from ourcup import basedir
from ourcup.fixtures.country_codes import CountryCodes

FIXTURES_JSON_FILE = os.path.join(basedir, 'ourcup', 'fixtures', 'data', 'world-cup-2019-matches.json')

logger = logging.getLogger(__name__)


class MatchPicker(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._json_file_path = FIXTURES_JSON_FILE
        self._fixtures = MatchPicker._process_matches(json.load(open(self._json_file_path)))
        self._logger.info("loading fixtures from "+self._json_file_path)
        self._translator = CountryCodes()

    @staticmethod
    def _process_matches(raw_match_data):
        matches = []
        for m in raw_match_data:
            team1_alpha3 = m['home_team']['code']
            team2_alpha3 = m['away_team']['code']
            # skip matches that we don't know the teams of yet
            if (team1_alpha3 != 'TBD') and (team2_alpha3 != 'TBD'):
                match = {
                    'team1': team1_alpha3,
                    'team2': team2_alpha3,
                    'date': m['datetime'][0:10]
                }
                matches.append(match)
        return matches

    def by_population(self, country_pop_data):
        all_games = copy.deepcopy(self._fixtures)
        # change the score so US doesn't show up very much, commented out because USA isn't in it!
        # country_alpha3_to_pop_map['USA'] = 1
        country_alpha3_to_pop_map = {m['country']: m['population'] for m in country_pop_data}
        for game in all_games:
            logger.debug("{} vs. {}".format(game['team1'], game['team2']))
            try:
                team1_pop = country_alpha3_to_pop_map[self._translator.getByFifaAlpha3(game['team1']).iso]
            except KeyError:
                logger.warning("Can't find population data for {}".format(game['team1']))
                team1_pop = 0  # the country isn't our list of
            try:
                team2_pop = country_alpha3_to_pop_map[self._translator.getByFifaAlpha3(game['team2']).iso]
            except KeyError:
                logger.warning("Can't find population data for {}".format(game['team2']))
                team2_pop = 0  # the country isn't our list of
            game['score'] = team1_pop + team2_pop

        prioritized_games = sorted(all_games, key=itemgetter('score'), reverse=True)
        for game in prioritized_games:
            game['team1Country'] = self._translator.getByFifaAlpha3(game['team1'])
            game['team2Country'] = self._translator.getByFifaAlpha3(game['team2'])
            game['date'] = datetime.datetime.strptime(game['date'], '%Y-%m-%d')
        return prioritized_games

    def participating_country_codes(self):
        team1_codes = set([game['team1'] for game in self._fixtures])
        team2_codes = set([game['team2'] for game in self._fixtures])
        combined = team1_codes.union(team2_codes)
        return combined
