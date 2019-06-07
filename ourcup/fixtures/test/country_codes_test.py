import unittest

from ourcup.fixtures.country_codes import CountryCodes


class CountryCodesTest(unittest.TestCase):

    def testCreate(self):
        translator = CountryCodes()
        self.assertEqual(translator.getByFifaAlpha3('BRA').iso, 'BRA')
        self.assertEqual(translator.getByFifaAlpha3('BRA').name, 'Brazil')
        self.assertEqual(translator.getByFifaAlpha3('NED').iso, 'NLD')
        self.assertEqual(translator.getByFifaAlpha3('BRA').emoji, '🇧🇷')
