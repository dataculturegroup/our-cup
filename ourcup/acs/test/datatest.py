import unittest
import os.path

from acs.population import PopulationDataManager
from acs.zip_code import ZipCodeDataManager


class PopulationDataManagerTest(unittest.TestCase):

    TEST_CSV_PATH = '/fixtures/ACS_12_5YR_B05006-MA/ACS_12_5YR_B05006_with_ann.csv'
    TEST_STATE = 'Massachusetts'
    TEST_COUNTY = 'Middlesex County'

    def testLoadFromStateCsv(self):
        data_set = PopulationDataManager()
        self.assertTrue(data_set is not None)
        data_set.loadFromStateCsvFile( os.path.dirname(os.path.realpath(__file__))+self.TEST_CSV_PATH )
        self.assertEqual(data_set.headers[0], 'GEO.id')
        self.assertEqual(data_set.headers[1], 'GEO.id2')
        self.assertEqual(data_set.sub_headers[0], 'Id')
        self.assertEqual(data_set.sub_headers[1], 'Id2')


class ZipCodeDataManagerTest(unittest.TestCase):

    TEST_CSV_PATH = '/fixtures/zcta_tract_rel_10-partial.csv'

    def testLoadFromCsv(self):
        dataset = ZipCodeDataManager()
        dataset.loadFromCsv(os.path.dirname(os.path.realpath(__file__))+self.TEST_CSV_PATH)
        self.assertEqual(len(dataset.records), 16)
        tract_02144 = [r for r in dataset.records if r.zip_code == '02144']
        self.assertEquals(len(tract_02144), 9)
        tract_02143 = [r for r in dataset.records if r.zip_code == '02143']
        self.assertEquals(len(tract_02143), 7)
        for record in dataset.records:
            self.assertEqual(record.state_id, '25')
            self.assertEqual(record.county_id, '017')
