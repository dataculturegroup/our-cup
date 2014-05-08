import unittest, os.path

import acs.data

class ForeignBornTest(unittest.TestCase):

    TEST_CSV_PATH = '/fixtures/ACS_12_5YR_B05006-MA/ACS_12_5YR_B05006_with_ann.csv'
    TEST_STATE = 'Massachusetts'
    TEST_COUNTY = 'Middlesex County'

    def testLoadFromStateCsv(self):
        dataset = acs.data.ForeignBorn()
        self.assertTrue(dataset is not None)
        dataset.loadFromStateCsvFile( os.path.dirname(os.path.realpath(__file__))+self.TEST_CSV_PATH )
        self.assertEqual(dataset.headers[0],'GEO.id')
        self.assertEqual(dataset.headers[1],'GEO.id2')
        self.assertEqual(dataset.subheaders[0],'Id')
        self.assertEqual(dataset.subheaders[1],'Id2')
