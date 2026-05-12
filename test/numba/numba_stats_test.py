import unittest
import numpy as np
import numba
import logging
import sys
from MuonDataLib.numba.stats import (get_bin_edges,
                                     para_histogram,
                                     get_max_threads)


class NumbaStatsTest(unittest.TestCase):

    def test_parallel(self):
        N = get_max_threads()

        log = logging.getLogger('TestStats.test_parallel')
        log.debug("")
        log.debug(f"{N} threads available")

        self.assertEqual(get_max_threads(),
                         numba.get_num_threads())

    def test_get_bin_edges_matches_numpy(self):
        """
        Get_bin_edges(min, max, delta)
        Should match np.arange(min, max + delta, delta) roughly
        but specifically it ensures max is the last element.
        """
        a_min, a_max, delta = 0.0, 10.0, 1.0
        edges = get_bin_edges(a_min, a_max, delta)
        expected = np.arange(0, 11, 1, dtype=np.float64)
        np.testing.assert_array_almost_equal(edges, expected)
        self.assertEqual(edges[-1], a_max)

    def test_para_histogram_ignores_out_of_range(self):
        times = np.array([0.5, 1.5, 2.5, 5.0, -1.0, 10.0], dtype=np.float64)
        spec = np.array([0, 0, 0, 0, 0, 0], dtype=np.int32)
        periods = np.array([0, 0, 0, 0, 0, 0], dtype=np.int32)
        weight = np.array([1, 1, 1, 1, 1, 1], dtype=np.int32)

        """
        min_time=0, max_time=3, width=1.0
        bins: [0, 1, 2, 3]
        Data points:
        0.5 -> bin 0
        1.5 -> bin 1
        2.5 -> bin 2
        5.0 -> ignore (>3)
        -1.0 -> ignore (<0)
        10.0 -> ignore (>3)
        """
        result, bins, N = para_histogram(
            times, spec, 1, periods, 1, weight,
            min_time=0.0, max_time=3.0, width=1.0,
            conversion=1.0, N_threads=2
        )

        # Expected result shape (N_periods, N_spec, N_bins) -> (1, 1, 3)
        self.assertEqual(result.shape, (1, 1, 3))
        np.testing.assert_array_equal(result[0, 0], [1, 1, 1])
        self.assertEqual(N, 3)

    def test_para_histogram_weights(self):
        times = np.array([0.5, 0.5, 1.5], dtype=np.float64)
        spec = np.array([0, 0, 0], dtype=np.int32)
        periods = np.array([0, 0, 0], dtype=np.int32)
        # one event has weight 0
        weight = np.array([1, 0, 1], dtype=np.int32)

        result, bins, N = para_histogram(
            times, spec, 1, periods, 1, weight,
            min_time=0.0, max_time=2.0, width=1.0,
            conversion=1.0, N_threads=2
        )

        np.testing.assert_array_equal(result[0, 0], [1, 1])
        self.assertEqual(N, 2)

    def test_para_histogram_conversion(self):
        # Data in ms, conversion to s
        times = np.array([500.0, 1500.0], dtype=np.float64)
        spec = np.array([0, 0], dtype=np.int32)
        periods = np.array([0, 0], dtype=np.int32)
        weight = np.array([1, 1], dtype=np.int32)

        result, bins, N = para_histogram(
            times, spec, 1, periods, 1, weight,
            min_time=0.0, max_time=2.0, width=1.0,
            conversion=1e-3, N_threads=2
        )

        """
        500ms * 1e-3 = 0.5s -> bin 0
        1500ms * 1e-3 = 1.5s -> bin 1
        """
        np.testing.assert_array_equal(result[0, 0], [1, 1])
        self.assertEqual(N, 2)

    def test_para_histogram_multi_spec_multi_period(self):
        """
        2 periods, 3 spectra
        times: [0.5, 1.5, 0.5, 1.5, 0.5, 1.5]
        spec:  [0, 1, 2, 0, 1, 2]
        periods: [0, 0, 0, 1, 1, 1]
        """
        times = np.array([0.5, 1.5, 0.5, 1.5, 0.5, 1.5], dtype=np.float64)
        spec = np.array([0, 1, 2, 0, 1, 2], dtype=np.int32)
        periods = np.array([0, 0, 0, 1, 1, 1], dtype=np.int32)
        weight = np.array([1, 1, 1, 1, 1, 1], dtype=np.int32)

        result, bins, N = para_histogram(
            times, spec, 3, periods, 2, weight,
            min_time=0.0, max_time=2.0, width=1.0,
            conversion=1.0, N_threads=2
        )

        # result shape (N_periods, N_spec, N_bins) -> (2, 3, 2)
        self.assertEqual(result.shape, (2, 3, 2))
        """
        Period 0:
        spec 0, time 0.5 -> result[0, 0, 0] = 1
        spec 1, time 1.5 -> result[0, 1, 1] = 1
        spec 2, time 0.5 -> result[0, 2, 0] = 1
        """
        self.assertEqual(result[0, 0, 0], 1)
        self.assertEqual(result[0, 1, 1], 1)
        self.assertEqual(result[0, 2, 0], 1)

        """
        Period 1:
        spec 0, time 1.5 -> result[1, 0, 1] = 1
        spec 1, time 0.5 -> result[1, 1, 0] = 1
        spec 2, time 1.5 -> result[1, 2, 1] = 1
        """
        self.assertEqual(result[1, 0, 1], 1)
        self.assertEqual(result[1, 1, 0], 1)
        self.assertEqual(result[1, 2, 1], 1)
        """
        Check the total number of events is 6,
        i.e. that all other elements are zero
        """
        self.assertEqual(np.sum(result), 6)
        self.assertEqual(N, 6)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestStats.test_parallel").setLevel(logging.DEBUG)
    unittest.main()
