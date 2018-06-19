import logging
import csv
import os
from collections import namedtuple
from iso3166 import countries

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TractPopulationRecord = namedtuple('TractPopulationRecord',
                                   ['id', 'id2', 'label', 'tract', 'county', 'state', 'country', 'pop_by_country'])


class PopulationDataManager(object):
    '''
    Wrapper around B05006 state census tract files (from American Census Fact Finder):
    PLACE OF BIRTH FOR THE FOREIGN-BORN POPULATION IN THE UNITED STATES
    Universe: Foreign-born population excluding population born at sea
    2008-2012 American Community Survey 5-Year Estimates
    '''

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.headers = None
        self.sub_headers = None
        self._buildColHeaderToAlpha2Map()   # how to parse any individual state CSV
        self._logger.debug('Created header map')
        self.records = []

    def loadAllStateCsvs(self, csv_abs_file_paths):
        for csv in csv_abs_file_paths:
            self.loadFromStateCsvFile(csv)

    def loadFromStateCsvFile(self, file_abs_path):
        self._logger.debug('  Loading data from '+file_abs_path)
        csv_file = open(file_abs_path, 'r', encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        self.headers = next(csv_reader)
        self.sub_headers = next(csv_reader)
        try:
            for row in csv_reader:
                pop_by_country = {}
                for col_name, alpha2 in iter(self._colHeaderToAlpha2Map.items()):
                    col_idx = self.headers.index(col_name)
                    pop_by_country[alpha2] = int(row[col_idx])
                label_parts = row[2].split(',')
                census_tract = label_parts[0].strip().replace('Census Tract', '')
                county = label_parts[1].strip()
                state = label_parts[2].strip()
                rec = TractPopulationRecord(row[0], row[1], row[2], census_tract, county, state, 'USA', pop_by_country)
                self.records.append(rec)
        except UnicodeDecodeError as ude:
            self._logger.error("Failed to import {}".format(row))
            self._logger.exception(ude)
        self._logger.debug('    done')

    def _buildColHeaderToAlpha2Map(self):
        self._colHeaderToAlpha2Map = {}
        # I created this lookup table by hand
        file_path = os.path.join(base_dir, 'acs', 'ACS_12_5YR_B05006_metadata-iso3166.csv')
        logging.debug("Loading header to alpha map from {}".format(file_path))
        csvfile = open(file_path, encoding='utf-8')
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if "Estimate" in row[1]:  # TODO: how to handle margin of error?
                try:
                    country_code = countries.get(row[2])
                    self._colHeaderToAlpha2Map[row[0]] = country_code.alpha3
                except:
                    continue
