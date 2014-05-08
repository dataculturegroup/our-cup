#! /usr/bin/env python

import unittest

from acs.test.datatest import ForeignBornTest
from worldcup.test.fixturestest import PickerTest, CountryCodeTranslatorTest

test_classes = [
	ForeignBornTest, PickerTest, CountryCodeTranslatorTest
]

for test_class in test_classes:
	suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
	unittest.TextTestRunner(verbosity=2).run(suite)
