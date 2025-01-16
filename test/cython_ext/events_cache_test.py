import unittest
import numpy as np
import datetime

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.events_cache import EventsCache


class EventsCacheTest(TestHelper):

    def setUp(self):
        self.date = datetime.datetime(2024, 11, 21, 7, 59, 0)
        self.cache = EventsCache(self.date, np.asarray([100], np.int32))

    def test_create_empty_cache(self):
        self.assertTrue(self.cache.empty())
        with self.assertRaises(RuntimeError):
            self.cache.get_histograms()
        with self.assertRaises(RuntimeError):
            self.cache.get_discarded_good_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_discarded_raw_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_good_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_raw_frames

    def test_save_to_cache(self):
        self.assertTrue(self.cache.empty())

        self.cache.save(np.asarray([[[1, 2, 3],
                                    [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32)
                        )

        self.assertFalse(self.cache.empty())
        hist, bins = self.cache.get_histograms()
        self.assertArrays(hist, [[[1, 2, 3],
                                  [4, 5, 6]]])
        self.assertArrays(bins, [7, 8, 9])
        self.assertArrays(self.cache.get_discarded_good_frames,
                          np.asarray([30], dtype=np.int32))
        self.assertArrays(self.cache.get_discarded_raw_frames,
                          np.asarray([20], dtype=np.int32))
        self.assertArrays(self.cache.get_good_frames,
                          np.asarray([70], dtype=np.int32))
        self.assertArrays(self.cache.get_raw_frames,
                          np.asarray([80], dtype=np.int32))

    def test_clear_cache(self):
        self.assertTrue(self.cache.empty())

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32))

        self.assertFalse(self.cache.empty())

        self.cache.clear()
        self.assertTrue(self.cache.empty())
        with self.assertRaises(RuntimeError):
            self.cache.get_histograms()
        with self.assertRaises(RuntimeError):
            self.cache.get_discarded_good_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_discarded_raw_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_good_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_raw_frames

    def test_set_too_many_filter_frames(self):
        self.assertTrue(self.cache.empty())

        with self.assertRaises(RuntimeError):
            self.cache.save(np.asarray([[[1, 2, 3],
                                         [4, 5, 6]]], dtype=np.int32),
                            np.asarray([7, 8, 9], dtype=np.double),
                            np.asarray([1, 2], dtype=np.int32),
                            np.asarray([1], dtype=np.int32))

    def test_set_too_many_veto_frames(self):
        self.assertTrue(self.cache.empty())

        with self.assertRaises(RuntimeError):
            self.cache.save(np.asarray([[[1, 2, 3],
                                         [4, 5, 6]]], dtype=np.int32),
                            np.asarray([7, 8, 9], dtype=np.double),
                            np.asarray([1], dtype=np.int32),
                            np.asarray([1, 20], dtype=np.int32))

    def test_duration(self):

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32))
        self.assertAlmostEqual(self.cache.get_count_duration, 1.75, 3)


if __name__ == '__main__':
    unittest.main()
