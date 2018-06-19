import unittest

from ourcup.fixtures.country_codes import CountryCodes


class CountryCodesTest(unittest.TestCase):

    def testCreate(self):
        translator = CountryCodes()
        self.assertEquals(translator.getByFifaCode('BRA').iso,'BRA')
        self.assertEquals(translator.getByFifaCode('BRA').name,'Brazil')
        self.assertEquals(translator.getByFifaCode('NED').iso,'NLD')
