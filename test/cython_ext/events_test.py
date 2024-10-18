import unittest
import numpy as np
import os
import json

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.event_data import Events
from MuonDataLib.cython_ext.events_cache import EventsCache


class EventsTest(TestHelper):

    def setUp(self):

        self._IDs = np.asarray([0, 1, 0, 1, 0, 1], dtype='int32')
        self._time = 1.e3*np.asarray([1., 2., 3., 4., 5., 6.], dtype=np.double)
        self._frame_i = np.asarray([0, 2, 4], dtype='int32')
        self._frame_time = np.asarray([0., 2., 4.], dtype=np.double)

        self._events = Events(self._IDs,
                              self._time,
                              self._frame_i,
                              self._frame_time,
                              2)

    def test_get_N_spec(self):
        self.assertEqual(self._events.get_N_spec, 2)

    def test_get_N_events(self):
        self.assertEqual(self._events.get_N_events, 6)

    def test_get_total_frames(self):
        self.assertEqual(self._events.get_total_frames, 3)

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

    def test_custom_histogram(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram(0., 7., 1.)
        self.assertArrays(bins, np.arange(0., 8., 1.))
        self.assertEqual(len(mat), 2)
        self.assertArrays(mat[0], [0, 1, 0, 1, 0, 1, 0])
        self.assertArrays(mat[1], [0, 0, 1, 0, 1, 0, 1])

    def test_cache_histogram(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())
        mat, bins = self._events.histogram(1.2, 4.2, .2, cache)

        self.assertFalse(cache.empty())
        c_mat, c_bins = cache.get_histograms()
        self.assertArrays(bins, c_bins)
        # cache adds a list for periods, need to remove it
        self.assertEqual(len(mat), len(c_mat[0]))

    def test_get_start_times(self):
        self.assertArrays(self._events.get_start_times(),
                          [0., 2., 4.])

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

    def test_save_filters(self):
        self._events.add_filter('test', 1.2, 5.2)
        self._events.add_filter('unit', 2.1, 2.6)
        self._events.save_filters('filter_data.json')

        with open('filter_data.json') as file:
            data = json.load(file)

        keys = list(data.keys())
        self.assertEqual(len(keys), 2)
        self.assertArrays(data['test'], [1.2, 5.2])
        self.assertArrays(data['unit'], [2.1, 2.6])

        os.remove('filter_data.json')

    def test_read_filter(self):
        f_start, f_end = self._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(len(keys), 0)

        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'load_filter.json')

        self._events.load_filters(file)

        f_start, f_end = self._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(keys[0], 'test')
        self.assertEqual(keys[1], 'unit')
        self.assertEqual(len(keys), 2)

        self.assertEqual(f_start['test'], 1.1)
        self.assertEqual(f_start['unit'], 3.1)
        self.assertEqual(f_end['test'], 8.2)
        self.assertEqual(f_end['unit'], 6.6)

    def test_report_filters(self):
        self._events.add_filter('test', 1.2, 5.2)
        self._events.add_filter('unit', 2.1, 2.6)

        data = self._events.report_filters()

        keys = list(data.keys())
        self.assertEqual(len(keys), 2)
        self.assertArrays(data['test'], [1.2, 5.2])
        self.assertArrays(data['unit'], [2.1, 2.6])

    def test_filter_histogram(self):
        self._events.add_filter('test', 1.2*1e-3, 2.3*1e-3)
        mat, bins = self._events.histogram(0., 7., 1.)
        self.assertArrays(bins, np.arange(0., 8., 1.))
        self.assertEqual(len(mat), 2)
        self.assertArrays(mat[0], [0, 0, 0, 1, 0, 1, 0])
        self.assertArrays(mat[1], [0, 0, 0, 0, 1, 0, 1])


if __name__ == '__main__':
    unittest.main()
