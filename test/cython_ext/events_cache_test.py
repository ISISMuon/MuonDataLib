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
                                [4, 5, 6]]], dtype=np.int32),
                   np.asarray([7, 8, 9], dtype=np.double),
                   np.asarray([1], dtype=np.int32))

        self.assertFalse(cache.empty())
        self.assertEqual(np.asarray(cache.get_total_frames()), [1])
        self.assertEqual(np.asarray(cache.get_good_frames()), [1])
        hist, bins = cache.get_histograms()
        self.assertArrays(hist, [[[1, 2, 3],
                                  [4, 5, 6]]])
        self.assertArrays(bins, [7, 8, 9])

    def test_clear_cache(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())

        cache.save(np.asarray([[[1, 2, 3],
                                [4, 5, 6]]], dtype=np.int32),
                   np.asarray([7, 8, 9], dtype=np.double),
                   np.asarray([1], dtype=np.int32))

        self.assertFalse(cache.empty())

        cache.clear()
        self.assertTrue(cache.empty())
        with self.assertRaises(RuntimeError):
            cache.get_histograms()
        with self.assertRaises(RuntimeError):
            cache.get_total_frames()

    def test_set_good_frames(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())
        cache.save(np.asarray([[[1, 2, 3],
                                [4, 5, 6]]], dtype=np.int32),
                   np.asarray([7, 8, 9], dtype=np.double),
                   np.asarray([10], dtype=np.int32))
        self.assertEqual(np.asarray(cache.get_good_frames()), [10])

        cache.set_good_frames(np.asarray([5], dtype=np.int32))

        self.assertEqual(np.asarray(cache.get_good_frames()), [5])
        self.assertEqual(np.asarray(cache.get_total_frames()), [10])

    def test_set_too_many_good_frames(self):
        cache = EventsCache()
        self.assertTrue(cache.empty())

        cache.save(np.asarray([[[1, 2, 3],
                                [4, 5, 6]]], dtype=np.int32),
                   np.asarray([7, 8, 9], dtype=np.double),
                   np.asarray([1], dtype=np.int32))

        with self.assertRaises(RuntimeError):
            cache.set_good_frames(np.asarray([1, 2], dtype=np.int32))


if __name__ == '__main__':
    unittest.main()
