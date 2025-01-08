import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.filter import (rm_overlaps,
                                           get_indices,
                                           good_values_ints,
                                           good_values_double)


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

    def test_get_indices(self):
        times = np.asarray([0, .1, .2, .3, .4, .5, .6, .7], dtype=np.double)
        f_start = np.asarray([0.14, 0.51], dtype=np.double)
        f_end = np.asarray([0.2, 0.59], dtype=np.double)

        j_start, j_end = get_indices(times,
                                     f_start,
                                     f_end)

        self.assertArrays(j_start, [1, 5])
        self.assertArrays(j_end, [2, 5])

    def test_good_values_ints(self):
        f_start = np.asarray([0, 4], dtype=np.int32)
        f_end = np.asarray([1, 4], dtype=np.int32)
        start_index = np.asarray([0, 10, 20, 30, 40], dtype=np.int32)
        int_array = np.arange(0, 45, dtype=np.int32)

        result = good_values_ints(f_start,
                                  f_end,
                                  start_index,
                                  int_array)
        self.assertEqual(len(result), 20)
        self.assertArrays(result, np.arange(20, 40))

    def test_good_values_double(self):
        f_start = np.asarray([0, 4], dtype=np.int32)
        f_end = np.asarray([1, 4], dtype=np.int32)
        start_index = np.asarray([0, 10, 20, 30, 40], dtype=np.int32)
        double_array = np.arange(0, 0.45, step=0.01, dtype=np.double)
        result = good_values_double(f_start,
                                    f_end,
                                    start_index,
                                    double_array)
        self.assertEqual(len(result), 20)
        self.assertArrays(result, np.arange(0.2, 0.4, step=0.01))


if __name__ == '__main__':
    unittest.main()
