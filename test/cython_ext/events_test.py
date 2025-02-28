import unittest
import numpy as np
import datetime

from MuonDataLib.data.utils import NONE
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.event_data import Events
from MuonDataLib.cython_ext.events_cache import EventsCache


class EventsTest(TestHelper):

    def setUp(self):

        self._IDs = np.asarray([0, 1, 0, 1, 0, 1], dtype='int32')
        self._time = 1.e3*np.asarray([1., 2., 3., 4., 5., 6.], dtype=np.double)
        self._frame_i = np.asarray([0, 2, 4], dtype='int32')
        self._frame_time = np.asarray([0.0, 2.0, 4.0], dtype=np.double)
        self._periods = np.zeros(len(self._frame_time), dtype=np.int32)
        self._events = Events(self._IDs,
                              self._time,
                              self._frame_i,
                              self._frame_time,
                              2,
                              self._periods)

    def test_get_N_spec(self):
        self.assertEqual(self._events.get_N_spec, 2)

    def test_get_N_events(self):
        self.assertEqual(self._events.get_N_events, 6)

    def test_get_total_frames(self):
        self.assertArrays(np.asarray(self._events.get_total_frames), [3])

    def test_histogram(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram()
        self.assertArrays(bins, np.arange(0, 32.784, 0.016))
        self.assertEqual(len(mat), 1)
        self.assertEqual(len(mat[0]), 2)

    def test_custom_histogram(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram(0., 7., 1.)
        self.assertArrays(bins, np.arange(0., 8., 1.))
        self.assertEqual(len(mat), 1)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 1, 0, 1, 0, 1, 0])
        self.assertArrays(mat[0][1], [0, 0, 1, 0, 1, 0, 1])

    def test_cache_histogram(self):
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))
        self.assertTrue(cache.empty())
        mat, bins = self._events.histogram(1.2, 4.2, .2, cache)

        self.assertFalse(cache.empty())
        c_mat, c_bins = cache.get_histograms()
        self.assertArrays(bins, c_bins)
        # cache adds a list for periods, need to remove it
        self.assertEqual(len(mat), len(c_mat))
        self.assertEqual(len(mat[0]), len(c_mat[0]))
        self.assertEqual(cache.get_good_frames[0], 100)
        self.assertEqual(cache.resolution, 0.2)
        self.assertEqual(cache.get_N_events, 3)

    def test_get_start_times(self):
        self.assertArrays(self._events.get_start_times(),
                          [0.0, 2.0, 4.0])

    def test_add_filter(self):
        f_start, f_end = self._events._get_filters()
        self.assertEqual(len(f_start.keys()), 0)
        self.assertEqual(len(f_end.keys()), 0)

        self._events.add_filter('test', 1.2, 5.2)
        self._events.add_filter('unit', 2.1, 2.6)

        f_start, f_end = self._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(keys[0], 'test')
        self.assertEqual(keys[1], 'unit')
        self.assertEqual(len(keys), 2)

        self.assertEqual(f_start['test'], 1.2)
        self.assertEqual(f_start['unit'], 2.1)
        self.assertEqual(f_end['test'], 5.2)
        self.assertEqual(f_end['unit'], 2.6)

    def test_add_filter_error(self):
        f_start, f_end = self._events._get_filters()
        self.assertEqual(len(f_start.keys()), 0)
        self.assertEqual(len(f_end.keys()), 0)

        self._events.add_filter('test', 1.2, 5.2)

        with self.assertRaises(RuntimeError):
            self._events.add_filter('test', 2.1, 2.6)

    def test_remove_filter(self):
        self._events.add_filter('test', 1.2, 5.2)
        self._events.add_filter('unit', 2.1, 2.6)

        f_start, f_end = self._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(len(keys), 2)

        self._events.remove_filter('test')

        f_start, f_end = self._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(len(keys), 1)

        self.assertEqual(keys[0], 'unit')
        self.assertEqual(f_start['unit'], 2.1)
        self.assertEqual(f_end['unit'], 2.6)

    def test_remove_filter_error(self):
        with self.assertRaises(RuntimeError):
            self._events.remove_filter('test')

    def test_clear_filters(self):
        self._events.add_filter('test', 1.2, 5.2)
        self._events.add_filter('unit', 2.1, 2.6)

        f_start, f_end = self._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(len(keys), 2)

        self._events.clear_filters()

        keys = list(f_start.keys())
        self.assertEqual(len(keys), 0)

        keys = list(f_end.keys())
        self.assertEqual(len(keys), 0)

    def test_report_filters(self):
        self._events.add_filter('test', 1.2, 5.2)
        self._events.add_filter('unit', 2.1, 2.6)

        data = self._events.report_filters()

        keys = list(data.keys())
        self.assertEqual(len(keys), 2)
        self.assertArrays(data['test'], [1.2, 5.2])
        self.assertArrays(data['unit'], [2.1, 2.6])

    def test_filter_histogram(self):
        self._events.add_filter('test', 1.2, 1.7)
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))
        mat, bins = self._events.histogram(0., 7., 1., cache)
        self.assertArrays(bins, np.arange(0., 8., 1.))
        self.assertEqual(len(mat), 1)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 0, 0, 1, 0, 1, 0])
        self.assertArrays(mat[0][1], [0, 0, 0, 0, 1, 0, 1])
        # check filter updates number of frames correctly
        self.assertEqual(cache.get_good_frames[0], 99)
        self.assertEqual(cache.get_N_events, 4)

    def test_filters_overlap_works(self):
        self._events.add_filter('test', 1.2, 1.7)
        self._events.add_filter('unit', 1.6, 1.9)
        date = datetime.datetime(2024, 12, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))
        mat, bins = self._events.histogram(0., 7., 1., cache)
        self.assertArrays(bins, np.arange(0., 8., 1.))
        self.assertEqual(len(mat), 1)
        self.assertEqual(len(mat[0]), 2)
        self.assertArrays(mat[0][0], [0, 0, 0, 1, 0, 1, 0])
        self.assertArrays(mat[0][1], [0, 0, 0, 0, 1, 0, 1])
        # check filter updates number of frames correctly
        self.assertEqual(cache.get_good_frames[0], 99)
        self.assertEqual(cache.get_N_events, 4)

    def test_get_filtered_data(self):
        self._events.add_filter('test', 1.2, 1.7)

        results = self._events._get_filtered_data(1.e-9*self._frame_time)
        f_start, f_end, rm, IDs, times, periods = results
        self.assertArrays(np.asarray(f_start), [0])
        self.assertArrays(np.asarray(f_end), [0])

        self.assertArrays(rm, [1])
        self.assertArrays(np.asarray(IDs), [0, 1, 0, 1])
        self.assertArrays(np.asarray(times), [3000., 4000.,
                                              5000., 6000.])

    def test_get_filtered_data_no_filter(self):

        results = self._events._get_filtered_data(1.e-9*self._frame_time)
        f_start, f_end, rm, IDs, times, periods = results
        self.assertArrays(np.asarray(f_start), [])
        self.assertArrays(np.asarray(f_end), [])

        self.assertArrays(rm, [0])
        self.assertArrays(np.asarray(IDs), [0, 1, 0, 1, 0, 1])
        self.assertArrays(np.asarray(times), [1000., 2000.,
                                              3000., 4000.,
                                              5000., 6000.])

    def test_get_filtered_data_no_data(self):
        self._events.add_filter('test', 0, 1e9)

        with self.assertRaises(ValueError):
            _ = self._events._get_filtered_data(1.e-9*self._frame_time)

    def test_start_and_end_times_filter_in_middle(self):
        frame_times = np.arange(1, 20, dtype=np.double)
        f_start = np.asarray([4, 16], dtype=np.int32)
        f_end = np.asarray([5, 17], dtype=np.int32)
        first, last = self._events._start_and_end_times(frame_times,
                                                        f_start,
                                                        f_end)
        self.assertEqual(first, 1.0)
        self.assertEqual(last, 19.0)

    def test_start_and_end_times_filter_at_start(self):
        frame_times = np.arange(1, 20, dtype=np.double)
        f_start = np.asarray([0, 7], dtype=np.int32)
        f_end = np.asarray([5, 8], dtype=np.int32)
        first, last = self._events._start_and_end_times(frame_times,
                                                        f_start,
                                                        f_end)
        self.assertEqual(first, 7.0)
        self.assertEqual(last, 19.0)

    def test_start_and_end_times_filter_at_end(self):
        frame_times = np.arange(1, 20, dtype=np.double)
        f_start = np.asarray([4, 18], dtype=np.int32)
        f_end = np.asarray([5, 18], dtype=np.int32)
        first, last = self._events._start_and_end_times(frame_times,
                                                        f_start,
                                                        f_end)
        self.assertEqual(first, 1.0)
        self.assertEqual(last, 18.0)

    def test_apply_log_filter_no_filter(self):
        name = "test"
        x = np.arange(0, 10., 0.1, dtype=np.double)
        y = 2.1*np.sin(1.6*x)
        min_ = NONE
        max_ = NONE
        self._events.apply_log_filter(name, x, y, min_, max_)

        filters = self._events.report_filters()
        self.assertEqual(len(filters), 0)

    def test_apply_log_filter_min_value(self):
        name = "test"
        x = np.arange(0, 10., 0.1, dtype=np.double)
        y = 2.1*np.sin(1.6*x)
        min_ = -1.1
        max_ = NONE
        self._events.apply_log_filter(name, x, y, min_, max_)

        filters = self._events.report_filters()
        self.assertEqual(len(filters), 3)

        expected_start = [0., 2.3, 6.2]
        expected_end = [0.1, 3.6, 7.6]
        for j, key in enumerate(filters.keys()):
            values = filters[key]
            # convert back to seconds from ns
            self.assertAlmostEqual(values[0]*1e-9, expected_start[j], 1)
            self.assertAlmostEqual(values[1]*1e-9, expected_end[j], 1)

    def test_apply_log_filter_max_value(self):
        name = "test"
        x = np.arange(0, 10., 0.1, dtype=np.double)
        y = 2.1*np.sin(1.6*x)
        min_ = NONE
        max_ = 1.2
        self._events.apply_log_filter(name, x, y, min_, max_)

        filters = self._events.report_filters()
        self.assertEqual(len(filters), 3)

        expected_start = [0.3, 4.3, 8.2]
        expected_end = [1.6, 5.6, 9.5]
        for j, key in enumerate(filters.keys()):
            values = filters[key]
            # convert back to seconds from ns
            self.assertAlmostEqual(values[0]*1e-9, expected_start[j], 1)
            self.assertAlmostEqual(values[1]*1e-9, expected_end[j], 1)

    def test_apply_log_filter_keep_ends_band(self):
        name = "test"
        x = np.arange(0, 10., 0.1, dtype=np.double)
        y = 2.1*np.sin(1.6*x)
        min_ = -1.1
        max_ = 1.2
        self._events.apply_log_filter(name, x, y, min_, max_)

        filters = self._events.report_filters()
        self.assertEqual(len(filters), 5)

        expected_start = [0.3, 2.3, 4.3, 6.2, 8.2]
        expected_end = [1.6, 3.6, 5.6, 7.6, 9.5]
        for j, key in enumerate(filters.keys()):
            values = filters[key]
            # convert back to seconds from ns
            self.assertAlmostEqual(values[0]*1e-9, expected_start[j], 1)
            self.assertAlmostEqual(values[1]*1e-9, expected_end[j], 1)

    def test_apply_log_filter_keep_middle_band(self):
        name = "test"
        x = np.arange(0, 10.001, 0.001, dtype=np.double)
        y = 2.1*x - 1.6
        min_ = 0.1
        max_ = 2.8
        self._events.apply_log_filter(name, x, y, min_, max_)

        filters = self._events.report_filters()
        self.assertEqual(len(filters), 2)

        expected_start = [0, 2.095]
        expected_end = [0.810, 10.000]
        expected_key = ['test_0', 'test_1']
        for j, key in enumerate(filters.keys()):
            self.assertEqual(key, expected_key[j])
            values = filters[key]
            # convert back to seconds from ns
            self.assertAlmostEqual(values[0]*1e-9, expected_start[j], 3)
            self.assertAlmostEqual(values[1]*1e-9, expected_end[j], 3)


if __name__ == '__main__':
    unittest.main()
