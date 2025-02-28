import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.filter import (rm_overlaps,
                                           good_periods,
                                           get_indices,
                                           good_values_ints,
                                           good_values_double,
                                           apply_filter)


class FilterTest(TestHelper):

    def test_one_frame_filter(self):
        i_start = np.asarray([1], dtype=np.int32)
        i_end = np.asarray([1], dtype=np.int32)
        periods = np.asarray([2, 1, 0], dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end, periods)
        self.assertArrays(j_start, [1])
        self.assertArrays(j_end, [1])
        self.assertArrays(N, np.asarray([0, 1, 0]))

    def test_two_frames_one_filter(self):
        i_start = np.asarray([1], dtype=np.int32)
        i_end = np.asarray([2], dtype=np.int32)
        periods = np.asarray([0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                             dtype=np.int32)
        j_start, j_end, N = rm_overlaps(i_start, i_end, periods)
        self.assertArrays(j_start, [1])
        self.assertArrays(j_end, [2])
        self.assertArrays(N, np.asarray([1, 1]))

    def test_two_frames_two_filters(self):
        i_start = np.asarray([1, 3], dtype=np.int32)
        i_end = np.asarray([1, 3], dtype=np.int32)
        periods = np.asarray([0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                             dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end, periods)
        self.assertArrays(j_start, [1, 3])
        self.assertArrays(j_end, [1, 3])
        self.assertArrays(N, np.asarray([0, 2]))

    def test_two_filters_overlap(self):
        i_start = np.asarray([1, 2], dtype=np.int32)
        i_end = np.asarray([2, 5], dtype=np.int32)
        periods = np.asarray([0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                             dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end, periods)
        self.assertArrays(j_start, [1])
        self.assertArrays(j_end, [5])
        self.assertArrays(N, np.asarray([2, 3]))

    def test_three_filters_one_overlap(self):
        i_start = np.asarray([1, 2, 8], dtype=np.int32)
        i_end = np.asarray([2, 5, 9], dtype=np.int32)
        periods = np.asarray([0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                             dtype=np.int32)

        j_start, j_end, N = rm_overlaps(i_start, i_end, periods)
        self.assertArrays(j_start, [1, 8])
        self.assertArrays(j_end, [5, 9])
        self.assertArrays(N, np.asarray([3, 4]))

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

    def test_apply_filter_unordered(self):
        x = np.arange(0, 10, dtype=np.double)
        y = 2.*x + 1
        times = [[8, 10], [0, 3]]
        fx, fy = apply_filter(x, y, times)
        # include the end of filter as it is within the band to keep
        self.assertArrays(fx, np.asarray([3, 4, 5, 6, 7], dtype=np.double))
        self.assertArrays(fy, np.asarray([7, 9, 11, 13, 15], dtype=np.double))

    def test_apply_filter_keep_middle(self):
        x = np.arange(0, 10, dtype=np.double)
        y = 2.*x + 1
        times = [[0, 3], [8, 10]]
        fx, fy = apply_filter(x, y, times)
        # include the end of filter as it is within the band to keep
        self.assertArrays(fx, np.asarray([3, 4, 5, 6, 7], dtype=np.double))
        self.assertArrays(fy, np.asarray([7, 9, 11, 13, 15], dtype=np.double))

    def test_apply_filter_keep_ends(self):
        x = np.arange(0, 10, dtype=np.double)
        y = 2.*x + 1
        times = [[1, 3.2], [5.1, 7.9]]
        fx, fy = apply_filter(x, y, times)
        self.assertArrays(fx, np.asarray([0, 4, 5, 9], dtype=np.double))
        self.assertArrays(fy, np.asarray([1, 9, 11, 19], dtype=np.double))

    def test_good_periods(self):
        f_start = np.asarray([0, 4], dtype=np.int32)
        f_end = np.asarray([1, 4], dtype=np.int32)
        start_index = np.asarray([0, 10, 20, 30, 40], dtype=np.int32)
        double_array = np.arange(0, 0.45, step=0.01, dtype=np.double)
        periods = np.asarray([0, 1, 1, 0, 1])
        result = good_periods(f_start,
                              f_end,
                              start_index,
                              periods,
                              len(double_array))
        self.assertEqual(len(result), 25)
        self.assertArrays(result, np.asarray([1, 1, 1,
                                              1, 1, 1,
                                              1, 1, 1,
                                              1, 0, 0,
                                              0, 0, 0,
                                              0, 0, 0,
                                              0, 0, 1,
                                              1, 1, 1, 1]))

    def test_good_periods_middle(self):
        f_start = np.asarray([4, 7], dtype=np.int32)
        f_end = np.asarray([5, 7], dtype=np.int32)
        start_index = np.asarray([0, 10, 20, 30, 40], dtype=np.int32)
        double_array = np.arange(0, 0.45, step=0.01, dtype=np.double)
        periods = np.asarray([0, 1, 1, 0, 1])
        result = good_periods(f_start,
                              f_end,
                              start_index,
                              periods,
                              len(double_array))
        self.assertEqual(len(result), 45)
        self.assertArrays(result, np.asarray([0, 0, 0,
                                              0, 0, 0,
                                              0, 0, 0,
                                              0, 1, 1,
                                              1, 1, 1,
                                              1, 1, 1,
                                              1, 1, 1,
                                              1, 1, 1,
                                              1, 1, 1,
                                              1, 1, 1,
                                              0, 0, 0,
                                              0, 0, 0,
                                              0, 0, 0,
                                              0, 1, 1,
                                              1, 1, 1]))


if __name__ == '__main__':
    unittest.main()
