import logging
import csv
from collections import namedtuple

TractZipCodeRecord = namedtuple('TractZipCodeRecord', ['zip_code', 'state_id', 'county_id', 'tract_id'])


class ZipCodeDataManager(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.headers = None
        self.subheaders = None
        self.records = []
        self._logger.debug("Create ZipCodeDataManager")

    def loadFromCsv(self, abs_csv_path):
        self._logger.debug("  loading from csv "+abs_csv_path)
        csvfile = open(abs_csv_path, encoding='utf-8')
        csvreader = csv.reader(csvfile)
        next(csvreader)    # dump header row
        self.records = [TractZipCodeRecord(row[0], row[1], row[2], row[3]) for row in csvreader]
        self._logger.debug("  loaded "+str(len(self.records))+" rows")
