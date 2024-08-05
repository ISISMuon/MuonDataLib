import unittest
import numpy as np

from MuonDataLib.cython_ext.event_data import mock_events
from MuonDataLib.test_helpers.unit_test import TestHelper


class EventsTest(TestHelper):

    def setUp(self):
        IDs, time, frame_i, events = mock_events()
        self._IDs = IDs
        self._time = time
        self._frame_i = frame_i
        self._events = events

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
        self.assertArrays(bins, np.arange(0, 30.5, 0.5))
        self.assertEqual(len(mat), 2)


if __name__ == '__main__':
    unittest.main()
