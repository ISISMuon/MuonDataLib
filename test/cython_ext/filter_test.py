import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.filter import (rm_overlaps,
                                           get_event_periods,
                                           get_indices,
                                           get_good_values,
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

    def test_get_good_values(self):
        f_start = np.asarray([0, 4], dtype=np.int32)
        f_end = np.asarray([1, 4], dtype=np.int32)
        start_index = np.asarray([0, 10, 20, 30, 40], dtype=np.int32)

        result = get_good_values(f_start,
                                 f_end,
                                 start_index,
                                 45)
        # the expected result corresponds to:
        # array = np.arange(0, 45, dtype=np.int32)
        # (array >= 20) & (array < 40)
        self.assertArrays(result, np.array([False, False, False, False, False,
                                            False, False, False, False, False,
                                            False, False, False, False, False,
                                            False, False, False, False, False,
                                            True, True, True, True, True,
                                            True, True, True, True, True,
                                            True, True, True, True, True,
                                            True, True, True, True, True,
                                            False, False, False, False, False])
                          )

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

    def test_get_event_periods(self):
        frame_periods = np.array([1, 2, 1], dtype=np.int32)
        start_index = np.array([1, 4, 6], dtype=np.int32)
        N_events = 8

        event_periods = get_event_periods(start_index, frame_periods, N_events)
        self.assertArrays(event_periods, np.array([1, 1, 1, 1, 2, 2, 1, 1]))


if __name__ == '__main__':
    unittest.main()
