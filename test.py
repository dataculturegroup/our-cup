#! /usr/bin/env python

import unittest

from ourcup.acs.test.datatest import PopulationDataManagerTest, ZipCodeDataManagerTest
from ourcup.fixtures.test.country_codes_test import CountryCodesTest
from ourcup.fixtures.test.match_picker_test import PickerTest
from ourcup.util.test.geo_test import GeoTest

test_classes = [
    PopulationDataManagerTest,
    ZipCodeDataManagerTest,
    PickerTest,
    CountryCodesTest,
    GeoTest
]

for test_class in test_classes:
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    unittest.TextTestRunner(verbosity=2).run(suite)
