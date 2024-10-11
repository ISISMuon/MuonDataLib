import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.event_data import Events
from MuonDataLib.cython_ext.events_cache import EventsCache


class EventsTest(TestHelper):

    def setUp(self):

        self._IDs = np.asarray([0, 1, 0, 1, 0, 1], dtype='int32')
        self._time = np.asarray([1., 2., 1., 2., 1., 2.], dtype=np.double)
        self._frame_i = np.asarray([0, 3], dtype='int32')
        self._frame_time = np.asarray([0., 5.], dtype=np.double)
        
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
        self.assertEqual(self._events.get_total_frames, 2)

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
        mat, bins = self._events.histogram(1.2, 4.2, .2)
        self.assertArrays(bins, np.arange(1.2, 4.4, 0.2))
        self.assertEqual(len(mat), 2)

    def test_cache_histogram(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())
        mat, bins = self._events.histogram(1.2, 4.2, .2, cache)

        self.assertFalse(cache.empty())
        c_mat, c_bins = cache.get_histograms()
        self.assertArrays(bins, c_bins)
        # cache adds a list for periods, need to remove it
        self.assertEqual(len(mat), len(c_mat[0]))


if __name__ == '__main__':
    unittest.main()
