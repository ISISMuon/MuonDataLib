import unittest
from numpy import array

from MuonDataLib.examples.add import add


class addTest(unittest.TestCase):
    def test_2_positive(self):
        LHS = array([1])
        RHS = array([2])

        result = add(LHS, RHS)

        self.assertEqual(result[0], 3)

    def test_2_negative(self):
        LHS = array([-1])
        RHS = array([-2])

        result = add(LHS, RHS)

        self.assertEqual(result[0], -3)

    def test_LHS_negative(self):
        LHS = array([-1])
        RHS = array([2])

        result = add(LHS, RHS)

        self.assertEqual(result[0], 1)

    def test_RHS_negative(self):
        LHS = array([1])
        RHS = array([-2])

        result = add(LHS, RHS)

        self.assertEqual(result[0], -1)

    def test_multiple_values(self):
        LHS = array([1, 2, 3])
        RHS = array([5, 6, 7])

        result = add(LHS, RHS)

        self.assertEqual(result[0], 6)
        self.assertEqual(result[1], 8)
        self.assertEqual(result[2], 10)

if __name__ == '__main__':
    unittest.main()
