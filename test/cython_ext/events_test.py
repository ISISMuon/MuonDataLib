import unittest
import numpy as np
import os

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.load_events import load_data


class EventsTest(TestHelper):

    def setUp(self):
        self._IDs = np.zeros(6, dtype=np.int32)
        for k in [1, 3, 5]:
            self._IDs[k] = 1
        self._time = np.asarray([1., 2., 1., 2., 1., 2.], dtype=np.double)
        self._frame_i = np.zeros(2, dtype=np.int32)
        self._frame_i[1] = 3

        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'simple_test.nxs')

        _, self._events = load_data(file)

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
