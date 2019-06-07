import unittest

from ourcup.fixtures.match_picker import MatchPicker


class PickerTest(unittest.TestCase):

    def testCreate(self):
        picker = MatchPicker()
        self.assertTrue(picker._fixtures is not None)

    def testParticipatingCountryCodes(self):
        picker = MatchPicker()
        countries = picker.participating_country_codes()
        self.assertEquals(len(countries), 24)

