import unittest
import numpy as np

from MuonDataLib.cython_ext.event_data import Events
from MuonDataLib.test_helpers.unit_test import TestHelper


class vector(object):
    """
    This is a simple wrapper to overwrite
    the len method.
    This is needed because Ubuntu returns
    the wrong data type from pure Python
    (long instead of int32)
    """
    def __new__(self, data, dtype):
        return np.asarray(data, dtype=dtype)

    def __len__(self):
        result = np.ndarray(len(self.data), dtype='int32')
        return result[0]


class EventsTest(TestHelper):

    def setUp(self):
        self._IDs = vector([0, 1, 0, 1, 0, 1], dtype='int32')
        self._time = np.asarray([1., 2., 1., 2., 1., 2.], dtype=np.double)
        self._frame_i = vector([0, 3], dtype='int32')
        self._events = Events(self._IDs,
                              self._time,
                              self._frame_i)

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
