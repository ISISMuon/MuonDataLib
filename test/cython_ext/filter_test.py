import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.filter import (rm_overlaps)


class FilterTest(TestHelper):

    def test_one_frame_filter(self):
        i_start = np.asarray([1], dtype=np.int32)
        i_end = np.asarray([1], dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end)
        self.assertArrays(j_start, [1])
        self.assertArrays(j_end, [1])
        self.assertEqual(N, 1)

    def test_two_frames_one_filter(self):
        i_start = np.asarray([1], dtype=np.int32)
        i_end = np.asarray([2], dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end)
        self.assertArrays(j_start, [1])
        self.assertArrays(j_end, [2])
        self.assertEqual(N, 2)

    def test_two_frames_two_filters(self):
        i_start = np.asarray([1, 3], dtype=np.int32)
        i_end = np.asarray([1, 3], dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end)
        self.assertArrays(j_start, [1, 3])
        self.assertArrays(j_end, [1, 3])
        self.assertEqual(N, 2)

    def test_two_filters_overlap(self):
        i_start = np.asarray([1, 2], dtype=np.int32)
        i_end = np.asarray([2, 5], dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end)
        self.assertArrays(j_start, [1])
        self.assertArrays(j_end, [5])
        self.assertEqual(N, 5)

    def test_three_filters_one_overlap(self):
        i_start = np.asarray([1, 2, 8], dtype=np.int32)
        i_end = np.asarray([2, 5, 9], dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end)
        self.assertArrays(j_start, [1, 8])
        self.assertArrays(j_end, [5, 9])
        self.assertEqual(N, 7)


if __name__ == '__main__':
    unittest.main()
