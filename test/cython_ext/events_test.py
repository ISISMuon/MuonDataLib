import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.event_data import Events


class EventsTest(TestHelper):

    def setUp(self):

        self._IDs = np.asarray([0, 1, 0, 1, 0, 1], dtype='int32')
        self._time = np.asarray([1., 2., 1., 2., 1., 2.], dtype=np.double)
        self._events = Events(self._IDs,
                              self._time)

    def test_get_N_spec(self):
        self.assertEqual(self._events.get_N_spec, 2)

    def test_get_N_events(self):
        self.assertEqual(self._events.get_N_events, 6)

    def test_get_filtered_events(self):
        self.assertArrays(self._events.get_filtered_events,
                          self._IDs)

    def test_histogram(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram()
        self.assertArrays(bins, np.arange(0, 32.780, 0.016))
        self.assertEqual(len(mat), 2)

    def test_histogram_options(self):
        """
        We dont check the histograms themselves
        as the stats_test.py covers them.
        Here we are checking that the correct values
        are passed to the histogram generation
        """
        mat, bins = self._events.histogram(min_time=1,
                                           max_time=10,
                                           width=1.)
        self.assertArrays(bins, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(len(mat), 2)


if __name__ == '__main__':
    unittest.main()
