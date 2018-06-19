import unittest

from ourcup.util.geo import reverse_geocode

SOMERVILLE_MA_LAT_LNG = [42.4000548, -71.122781]


class GeoTest(unittest.TestCase):

    def testReverseGeocode(self):
        results = reverse_geocode(SOMERVILLE_MA_LAT_LNG[0], SOMERVILLE_MA_LAT_LNG[1])
        self.assertEqual(results['County']['name'], "Middlesex")
        self.assertEqual(results['State']['code'], "MA")
        self.assertEqual(results['Block']['FIPS'], "250173505002001")
