from MuonDataLib.data.utils import (convert_date_for_NXS,
                                    convert_date,
                                    stype)
import unittest
import datetime


class UtilsTest(unittest.TestCase):

    def test_stype(self):
        self.assertEqual(stype('testing'), 'S8')

    def test_convert_date(self):
        date = '2018-12-24T13:32:01'
        date = convert_date(date)
        self.assertEqual(date, datetime.datetime(2018, 12, 24, 13, 32, 1))

    def test_convert_date_for_NXS(self):
        date = datetime.datetime(2018, 12, 24, 13, 32, 1)
        date = convert_date_for_NXS(date)
        self.assertEqual(date, '2018-12-24T13:32:01')


if __name__ == '__main__':
    unittest.main()
