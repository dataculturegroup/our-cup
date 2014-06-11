import json, os, logging, csv
from operator import itemgetter

class Picker(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._json_file_path = os.path.dirname(os.path.realpath(__file__))+'/data/world_cup_2014_games.json'
        self._fixtures = json.load(open(self._json_file_path))
        self._logger.info("loaded from "+self._json_file_path)
        self._translator = CountryCodeTranslator()
        
    def by_population(self, country_alpha3_to_pop_map):
        all_games = json.load(open(self._json_file_path))
        country_alpha3_to_pop_map['USA'] = 1 # juice the numbers
        for game in all_games:
            team1_pop = country_alpha3_to_pop_map[self._translator.fifa2iso(game['team1'])]
            team2_pop = country_alpha3_to_pop_map[self._translator.fifa2iso(game['team2'])]
            game['score'] = team1_pop + team2_pop
        prioritized_games = sorted(all_games, key=itemgetter('score'), reverse=True)
        return prioritized_games

    def participating_fifa_country_codes(self):
        return set([game['team1'] for game in self._fixtures] + [game['team2'] for game in self._fixtures])

class CountryCodeTranslator(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._csv_file_path = os.path.dirname(os.path.realpath(__file__))+'/data/ioc-fifa-iso-alpha3.csv'
        csvfile = open(self._csv_file_path, 'rb')
        csvreader = csv.reader(csvfile)
        self._headers = csvreader.next()
        self._fifa2iso = {}
        for row in csvreader:
            self._fifa2iso[row[2]] = row[3]
        self._logger.debug('Loaded data from '+self._csv_file_path)

    def fifa2iso(self, fifa_alpha3):
        '''
        Sourced from http://simple.wikipedia.org/wiki/Comparison_of_IOC,_FIFA,_and_ISO_3166_country_codes
        '''
        return self._fifa2iso[fifa_alpha3]
