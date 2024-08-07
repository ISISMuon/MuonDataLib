import unittest
import numpy as np
from MuonDataLib.cython_ext.stats import make_histogram
from MuonDataLib.test_helpers.unit_test import TestHelper


class StatsTest(TestHelper):

    def test_make_histogram_1_spec(self):
        times = np.asarray([1, 2, 3, 4, 1, 2, 3, 1, 2], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 1, 0, 5, 1, conversion=1.)
        self.assertArrays(bins, [0, 1, 2, 3, 4, 5])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [0, 3, 3, 2, 1])

    def test_make_histogram_1_spec_nonzero_start(self):
        times = np.asarray([1, 2, 3, 4, 1, 2, 3, 1, 2], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 1, 1, 5, 1, conversion=1.)
        self.assertArrays(bins, [1, 2, 3, 4, 5])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [3, 3, 2, 1])

    def test_make_histogram_1_spec_negative_start(self):
        times = np.asarray([1, 2, 3, 4, 1, 2, 3, 1, 2, -.4], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 1, -1, 5, 1, conversion=1.)
        self.assertArrays(bins, [-1, 0, 1, 2, 3, 4, 5])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [1, 0, 3, 3, 2, 1])

    def test_make_histogram_bin_edges(self):
        times = np.asarray([1, 1.5, 1.9, 2], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 1, 0, 5, 1, conversion=1.)
        self.assertArrays(bins, [0, 1, 2, 3, 4, 5])
        self.assertEqual(len(result), 1)
        # each bin should only include the left bin edge
        self.assertArrays(result[0], [0, 3, 1, 0, 0])

    def test_make_histogram_ignore_out_of_range_data(self):
        times = np.asarray([1.1, 1.5, 1.9, 2.1, -.1, 5.1], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 1, 0, 5, 1, conversion=1.)
        self.assertArrays(bins, [0, 1, 2, 3, 4, 5])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [0, 3, 1, 0, 0])

    def test_make_histogram_negative_end_time(self):
        times = np.asarray([-5, -4, -3, -5], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 1, -5, -2, 1, conversion=1.)
        self.assertArrays(bins, [-5, -4, -3, -2])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [2, 1, 1])

    def test_make_histogram_non_int(self):
        times = np.asarray([0.1, 0.2, 0.31, 0.1, 0.2, 0.1], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs,
                                      1, 0, 0.4, width=.10,
                                      conversion=1.)
        self.assertArrays(bins, [0, .1, .2, .3, .4])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [0, 30, 20, 10])

    def test_make_histogram_conversion(self):
        times = np.asarray([1, 2, 3, 4, 1, 2, 3, 1, 2], dtype=np.double)
        IDs = np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)

        result, bins = make_histogram(times, IDs,
                                      1, 0, 0.5, .1, conversion=0.1)
        self.assertArrays(bins, [0, .1, .2, .3, .4, .5])
        self.assertEqual(len(result), 1)
        self.assertArrays(result[0], [0, 30, 30, 20, 10])

    def test_make_histogram_multi_spec(self):
        times = np.asarray([1, 2, 3, 4, 1, 2, 3, 1, 2], dtype=np.double)
        IDs = np.asarray([0, 1, 2, 3, 0, 1, 2, 0, 1], dtype=np.int32)

        result, bins = make_histogram(times, IDs, 4, 0, 5, 1, conversion=1.)
        self.assertArrays(bins, [0, 1, 2, 3, 4, 5])
        self.assertEqual(len(result), 4)
        self.assertArrays(result[0], [0, 3, 0, 0, 0])
        self.assertArrays(result[1], [0, 0, 3, 0, 0])
        self.assertArrays(result[2], [0, 0, 0, 2, 0])
        self.assertArrays(result[3], [0, 0, 0, 0, 1])


if __name__ == '__main__':
    unittest.main()
