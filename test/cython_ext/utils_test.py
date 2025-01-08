import unittest
import numpy as np
from MuonDataLib.cython_ext.utils import binary_search
from MuonDataLib.test_helpers.unit_test import TestHelper


class UtilsTest(TestHelper):

    def test_simple_search(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)

        result = binary_search(times, 0, len(times), 5)
        self.assertEqual(result, 2)

    def test_target_is_start_value(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)

        result = binary_search(times, 0, len(times), 0)
        self.assertEqual(result, 0)

    def test_target_is_matched_value(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)

        result = binary_search(times, 0, len(times), 6)
        self.assertEqual(result, 3)

    def test_target_is_end_value(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)

        result = binary_search(times, 0, len(times), 14)
        self.assertEqual(result, 6)

    def test_target_is_after_gap(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)

        result = binary_search(times, 0, len(times), 13.1)
        self.assertEqual(result, 5)

    def test_target_is_exact_match(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)

        result = binary_search(times, 0, len(times), 12)
        self.assertEqual(result, 5)

    def test_target_is_too_small(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)
        with self.assertRaises(RuntimeError):
            _ = binary_search(times, 0, len(times), -12)

    def test_target_is_too_large(self):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)
        with self.assertRaises(RuntimeError):
            _ = binary_search(times, 0, len(times), 250)


if __name__ == '__main__':
    unittest.main()
