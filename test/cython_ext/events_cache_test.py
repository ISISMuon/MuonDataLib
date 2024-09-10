import unittest
import numpy as np

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.events_cache import EventsCache


class EventsCacheTest(TestHelper):

    def test_create_empty_cache(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())
        with self.assertRaises(RuntimeError):
            cache.get_histograms()
        with self.assertRaises(RuntimeError):
            cache.get_total_frames()

    def test_save_to_cache(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())

        cache.save(np.asarray([[[1, 2, 3],
                                [4, 5, 6]]]),
                   np.asarray([7, 8, 9], dtype=np.double),
                   1)

        self.assertFalse(cache.empty())
        self.assertEqual(cache.get_total_frames(), 1)
        hist, bins = cache.get_histograms()
        self.assertArrays(hist, [[[1, 2, 3],
                                  [4, 5, 6]]])
        self.assertArrays(bins, [7, 8, 9])

    def test_clear_cache(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())

        cache.save(np.asarray([[[1, 2, 3],
                                [4, 5, 6]]]),
                   np.asarray([7, 8, 9], dtype=np.double),
                   1)

        self.assertFalse(cache.empty())

        cache.clear()
        self.assertTrue(cache.empty())
        with self.assertRaises(RuntimeError):
            cache.get_histograms()
        with self.assertRaises(RuntimeError):
            cache.get_total_frames()


if __name__ == '__main__':
    unittest.main()
