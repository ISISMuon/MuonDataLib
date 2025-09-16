import unittest
import numpy as np
import datetime

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.event_data import Events
from MuonDataLib.cython_ext.events_cache import EventsCache


class MultiperiodEventsTest(TestHelper):
    """
    Will only test the bits of the event class that
    are changed by the inclusion of multiple
    periods. Since the events_test.py file
    covers the rest of the functionality.
    """
    def setUp(self):

        self._IDs = np.asarray([0, 1, 0, 1, 0, 1, 0, 1], dtype='int32')
        self._time = 1.e3*np.asarray([1., 2., 3., 4., 5.,
                                      6., 7., 8.], dtype=np.double)
        self._frame_i = np.asarray([0, 2, 4, 6], dtype='int32')
        self._frame_time = np.asarray([0.0, 2.0, 4.0, 6.0], dtype=np.double)
        self._periods = np.asarray([0, 1, 0, 1], dtype=np.int32)
        self._amps = np.asarray([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
                                dtype=np.double)
        self._events = Events(self._IDs,
                              self._time,
                              self._frame_i,
                              self._frame_time,
                              2,
                              self._periods,
                              self._amps)

    def test_histogram(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram()
        self.assertArrays(bins, np.arange(0, 32.784, 0.016))
        self.assertEqual(len(mat), 2)
        self.assertEqual(len(mat[0]), 2)

    def test_custom_histogram(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram(0., 9., 1.)
        self.assertArrays(bins, np.arange(0., 10., 1.))
        self.assertEqual(len(mat), 2)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 1, 0, 0, 0, 1, 0, 0, 0])
        self.assertArrays(mat[0][1], [0, 0, 1, 0, 0, 0, 1, 0, 0])
        self.assertArrays(mat[1][0], [0, 0, 0, 1, 0, 0, 0, 1, 0])
        self.assertArrays(mat[1][1], [0, 0, 0, 0, 1, 0, 0, 0, 1])

    def test_cache_histogram(self):
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100, 100], dtype=np.int32))
        self.assertTrue(cache.empty())
        mat, bins = self._events.histogram(1.2, 8.2, .2, cache)

        self.assertFalse(cache.empty())
        c_mat, c_bins = cache.get_histograms()
        self.assertArrays(bins, c_bins)
        self.assertEqual(len(mat), len(c_mat))
        self.assertEqual(len(mat[0]), len(c_mat[0]))
        self.assertEqual(cache.get_good_frames[0], 100)
        self.assertEqual(cache.resolution, 0.2)
        self.assertEqual(cache.get_N_events, 7)

    def test_filter_histogram_period_1(self):
        self._events.add_filter('test', 1.2, 1.7)
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100, 100], dtype=np.int32))
        mat, bins = self._events.histogram(0., 9., 1., cache)
        self.assertArrays(bins, np.arange(0., 10., 1.))
        self.assertEqual(len(mat), 2)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 0, 0, 0, 0, 1, 0, 0, 0])
        self.assertArrays(mat[0][1], [0, 0, 0, 0, 0, 0, 1, 0, 0])
        self.assertArrays(mat[1][0], [0, 0, 0, 1, 0, 0, 0, 1, 0])
        self.assertArrays(mat[1][1], [0, 0, 0, 0, 1, 0, 0, 0, 1])

        # check filter updates number of frames correctly
        self.assertArrays(cache.get_good_frames, np.asarray([99, 100]))
        self.assertEqual(cache.get_N_events, 6)

    def test_filter_histogram_period_2(self):
        self._events.add_filter('test', 6.2, 8.7)
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100, 100], dtype=np.int32))
        mat, bins = self._events.histogram(0., 9., 1., cache)
        self.assertArrays(bins, np.arange(0., 10., 1.))
        self.assertEqual(len(mat), 2)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 1, 0, 0, 0, 1, 0, 0, 0])
        self.assertArrays(mat[0][1], [0, 0, 1, 0, 0, 0, 1, 0, 0])
        self.assertArrays(mat[1][0], [0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertArrays(mat[1][1], [0, 0, 0, 0, 1, 0, 0, 0, 0])

        # check filter updates number of frames correctly
        self.assertArrays(cache.get_good_frames, np.asarray([100, 99]))
        self.assertEqual(cache.get_N_events, 6)

    def test_filter_histogram_both_periods(self):
        self._events.add_filter('test', 4.2, 6.2)
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100, 100], dtype=np.int32))
        mat, bins = self._events.histogram(0., 9., 1., cache)
        self.assertArrays(bins, np.arange(0., 10., 1.))
        self.assertEqual(len(mat), 2)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 1, 0, 0, 0, 0, 0, 0, 0])
        self.assertArrays(mat[0][1], [0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.assertArrays(mat[1][0], [0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertArrays(mat[1][1], [0, 0, 0, 0, 1, 0, 0, 0, 0])

        # check filter updates number of frames correctly
        self.assertArrays(cache.get_good_frames, np.asarray([99, 99]))
        self.assertEqual(cache.get_N_events, 4)
        """
        After this will only test both periods being filtered
        """

    def test_filters_overlap_works(self):
        self._events.add_filter('test', 5.2, 6.3)
        self._events.add_filter('unit', 4.2, 5.9)
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100, 100], dtype=np.int32))
        mat, bins = self._events.histogram(0., 9., 1., cache)
        self.assertArrays(bins, np.arange(0., 10., 1.))
        self.assertEqual(len(mat), 2)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 1, 0, 0, 0, 0, 0, 0, 0])
        self.assertArrays(mat[0][1], [0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.assertArrays(mat[1][0], [0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertArrays(mat[1][1], [0, 0, 0, 0, 1, 0, 0, 0, 0])
        # check filter updates number of frames correctly
        self.assertArrays(cache.get_good_frames, [99, 99])
        self.assertEqual(cache.get_N_events, 4)

    def test_get_filtered_data(self):
        self._events.add_filter('test', 1.2, 1.7)

        results = self._events._get_filtered_data(1.e-9*self._frame_time)
        f_start, f_end, rm, IDs, times, periods, amps = results
        self.assertArrays(np.asarray(f_start), [0])
        self.assertArrays(np.asarray(f_end), [0])

        self.assertArrays(rm, [1, 0])
        self.assertArrays(np.asarray(amps), [1.2, 1.3, 1.4, 1.5, 1.6, 1.7])
        self.assertArrays(np.asarray(IDs), [0, 1, 0, 1, 0, 1])
        self.assertArrays(np.asarray(times), [3000., 4000.,
                                              5000., 6000.,
                                              7000., 8000.])
        self.assertArrays(np.asarray(periods), [1, 1,
                                                0, 0,
                                                1, 1])

    def test_get_filtered_data_no_filter(self):

        results = self._events._get_filtered_data(1.e-9*self._frame_time)
        f_start, f_end, rm, IDs, times, periods, amps = results
        self.assertArrays(np.asarray(f_start), [])
        self.assertArrays(np.asarray(f_end), [])

        self.assertArrays(rm, [0, 0])
        self.assertArrays(np.asarray(IDs), [0, 1, 0, 1, 0, 1, 0, 1])
        self.assertArrays(np.asarray(amps), [1.0, 1.1, 1.2, 1.3,
                                             1.4, 1.5, 1.6, 1.7])
        self.assertArrays(np.asarray(times), [1000., 2000.,
                                              3000., 4000.,
                                              5000., 6000.,
                                              7000., 8000.])
        self.assertArrays(np.asarray(periods), [0, 0,
                                                1, 1,
                                                0, 0,
                                                1, 1])

    def test_get_total_frames(self):
        self.assertArrays(self._events.get_total_frames, [2, 2])


if __name__ == '__main__':
    unittest.main()
