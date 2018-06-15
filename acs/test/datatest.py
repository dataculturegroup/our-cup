import unittest, os.path

import acs.data


class PopulationDataManagerTest(unittest.TestCase):

    TEST_CSV_PATH = '/fixtures/ACS_12_5YR_B05006-MA/ACS_12_5YR_B05006_with_ann.csv'
    TEST_STATE = 'Massachusetts'
    TEST_COUNTY = 'Middlesex County'

    def testLoadFromStateCsv(self):
        dataset = acs.data.PopulationDataManager()
        self.assertTrue(dataset is not None)
        dataset.loadFromStateCsvFile( os.path.dirname(os.path.realpath(__file__))+self.TEST_CSV_PATH )
        self.assertEqual(dataset.headers[0],'GEO.id')
        self.assertEqual(dataset.headers[1],'GEO.id2')
        self.assertEqual(dataset.sub_headers[0], 'Id')
        self.assertEqual(dataset.sub_headers[1], 'Id2')


class ZipCodeDataManagerTest(unittest.TestCase):

    TEST_CSV_PATH = '/fixtures/zcta_tract_rel_10-partial.csv'

    def testLoadFromCsv(self):
        dataset = acs.data.ZipCodeDataManager()
        dataset.loadFromCsv( os.path.dirname(os.path.realpath(__file__))+self.TEST_CSV_PATH )
        self.assertEqual(len(dataset.records),16)
        zeroTwoOneFourFourTracts = [r for r in dataset.records if r.zip_code=='02144']
        self.assertEquals(len(zeroTwoOneFourFourTracts),9)
        zeroTwoOneFourThreeTracts = [r for r in dataset.records if r.zip_code=='02143']
        self.assertEquals(len(zeroTwoOneFourThreeTracts),7)
        for record in dataset.records:
            self.assertEqual(record.state_id, '25')
            self.assertEqual(record.county_id, '017')
