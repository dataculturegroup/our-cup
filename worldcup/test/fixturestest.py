import unittest, os.path

import worldcup.fixtures

class PickerTest(unittest.TestCase):

    #def setUp(self):
        #self._config = ConfigParser.ConfigParser()

    def testCreate(self):
        picker = worldcup.fixtures.Picker()
        self.assertTrue(picker._fixtures is not None)

class CountryCodeTranslatorTest(unittest.TestCase):

    def testCreate(self):
        translator = worldcup.fixtures.CountryCodeTranslator()
        self.assertEquals(translator.fifa2iso('BRA'),'BRA')
        self.assertEquals(translator.fifa2iso('NED'),'NLD')
