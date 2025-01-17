import unittest
from unittest import mock
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

    @mock.patch('MuonDataLib.cython_ext.utils.warning')
    def test_target_is_too_small_default(self, warning_mock):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)
        result = binary_search(times, 0, len(times), -12)
        self.assertEqual(result, 0)
        self.assertEqual(warning_mock.call_count, 1)
        msg = ("The target -12.0 is before the first value 0.0 . "
               "Difference is 12.0 ")
        warning_mock.assert_called_with(msg)

    @mock.patch('MuonDataLib.cython_ext.utils.warning')
    def test_target_is_too_large_default(self, warning_mock):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)
        result = binary_search(times, 0, len(times), 250)
        self.assertEqual(result, 6)
        self.assertEqual(warning_mock.call_count, 1)
        msg = ("The target 250.0 is after the last value 14.0 . "
               "Difference is 236.0 ")
        warning_mock.assert_called_with(msg)

    @mock.patch('MuonDataLib.cython_ext.utils.warning')
    def test_target_is_too_small(self, warning_mock):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)
        result = binary_search(times, 0, len(times), -12, 'Temp', 'K')
        self.assertEqual(result, 0)
        self.assertEqual(warning_mock.call_count, 1)
        msg = ("The target -12.0 is before the first Temp 0.0 K. "
               "Difference is 12.0 K")
        warning_mock.assert_called_with(msg)

    @mock.patch('MuonDataLib.cython_ext.utils.warning')
    def test_target_is_too_large(self, warning_mock):
        times = np.asarray([0, 2, 4, 6, 10, 12, 14], dtype=np.double)
        result = binary_search(times, 0, len(times), 250, 'Temp', 'K')
        self.assertEqual(result, 6)
        self.assertEqual(warning_mock.call_count, 1)
        msg = ("The target 250.0 is after the last Temp 14.0 K. "
               "Difference is 236.0 K")
        warning_mock.assert_called_with(msg)


if __name__ == '__main__':
    unittest.main()
