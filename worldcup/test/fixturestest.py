import unittest, os.path

import worldcup.fixtures

class PickerTest(unittest.TestCase):

    def testCreate(self):
        picker = worldcup.fixtures.Picker()
        self.assertTrue(picker._fixtures is not None)

    def testParticipatingFifaCountryCodes(self):
    	picker = worldcup.fixtures.Picker()
    	countries = picker.participating_fifa_country_codes()
    	self.assertEquals(len(countries),32)

class CountryCodeTranslatorTest(unittest.TestCase):

    def testCreate(self):
        translator = worldcup.fixtures.CountryCodeTranslator()
        self.assertEquals(translator.fifa2iso('BRA'),'BRA')
        self.assertEquals(translator.fifa2iso('NED'),'NLD')
