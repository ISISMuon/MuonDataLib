import unittest
from MuonDataLib.cython_ext.add import my_add


class AddTest(unittest.TestCase):

    def test_add(self):
        self.assertEqual(5, my_add(3, 2))


if __name__ == '__main__':
    unittest.main()
