import logging, csv, os
from collections import namedtuple
from iso3166 import countries

CensusTractRecord = namedtuple('CensusTractRecord',['id','id2','label','tract','county','state','country','pop_by_country'])

class ForeignBorn(object):
    '''
    Wrapper around B05006 state census tract files (from American Census Fact Finder):
    PLACE OF BIRTH FOR THE FOREIGN-BORN POPULATION IN THE UNITED STATES
    Universe: Foreign-born population excluding population born at sea
    2008-2012 American Community Survey 5-Year Estimates
    '''

    DATA_DIR_NAME = "ACS_12_5YR_B05006"
    DATA_FILE_NAME = "ACS_12_5YR_B05006_with_ann.csv"

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.headers = None
        self.subheaders = None
        self._buildColHeaderToAlpha2Map()   # how to parse any individual state CSV
        self._logger.debug('Created header map')
        self.records = []

    def loadAllStateCsvs(self,directory):
        self.loadFromStateCsvFile('data/ACS_12_5YR_B05006-A/ACS_12_5YR_B05006_with_ann.csv')
        self.loadFromStateCsvFile('data/ACS_09_5YR_B05006-B/ACS_09_5YR_B05006_with_ann.csv')

    def loadFromStateCsvFile(self,filepath):
        self._logger.debug('  Loading data from '+filepath)
        csvfile = open(filepath, 'rb')
        csvreader = csv.reader(csvfile)
        self.headers = csvreader.next()
        self.subheaders = csvreader.next()
        for row in csvreader:
            pop_by_country = {}
            for col_name, alpha2 in self._colHeaderToAlpha2Map.iteritems():
                col_idx = self.headers.index(col_name)
                pop_by_country[alpha2] = int(row[col_idx])
            label_parts = row[2].split(',')
            census_tract = label_parts[0].strip().replace('Census Tract','')
            county = label_parts[1].strip()
            state = label_parts[2].strip()
            rec = CensusTractRecord(row[0],row[1],row[2],census_tract,county,state,'USA',pop_by_country)
            self.records.append(rec)
        self._logger.debug('    done')

    def _buildColHeaderToAlpha2Map(self):
        self._colHeaderToAlpha2Map = {}
        csvfile = open( os.path.dirname(os.path.realpath(__file__))
            +'/ACS_12_5YR_B05006_metadata-iso3166.csv' )
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if "Estimate" in row[1]: #TODO: how to handle margin of error?
                try:
                    country_code = countries.get(row[2])
                    self._colHeaderToAlpha2Map[row[0]] = country_code.alpha3
                except:
                    continue
