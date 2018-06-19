import csv
import logging
import os
from collections import namedtuple

from ourcup import basedir

FIFA_ISO_LOOKUP = os.path.join(basedir, 'ourcup', 'fixtures', 'data', 'ioc-fifa-iso-alpha3.csv')

FifaCountryCodeRecord = namedtuple('FifaCountryCodeRecord', ['name', 'ioc', 'fifa', 'iso'])


class CountryCodes(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._csv_file_path = FIFA_ISO_LOOKUP
        csvfile = open(self._csv_file_path, 'r')
        csvreader = csv.reader(csvfile)
        self._headers = next(csvreader)
        self._fifa2info = {}
        for row in csvreader:
            self._fifa2info[row[2]] = FifaCountryCodeRecord(row[0], row[1], row[2], row[3])
        self._logger.debug('Loaded data from '+self._csv_file_path)

    def getByFifaCode(self, fifa_alpha3):
        '''
        Sourced from http://simple.wikipedia.org/wiki/Comparison_of_IOC,_FIFA,_and_ISO_3166_country_codes
        '''
        return self._fifa2info[fifa_alpha3]
