import unittest
import numpy as np
import datetime

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.cython_ext.events_cache import EventsCache
from MuonDataLib.data.utils import convert_date_for_NXS


class EventsCacheTest(TestHelper):

    def setUp(self):
        self.date = datetime.datetime(2024, 11, 21, 7, 59, 0)
        self.cache = EventsCache(self.date, np.asarray([100], np.int32))

    def test_create_empty_cache(self):
        self.assertTrue(self.cache.empty())
        with self.assertRaises(RuntimeError):
            self.cache.get_histograms()
        with self.assertRaises(RuntimeError):
            self.cache.get_discarded_raw_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_good_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_raw_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_resolution()

    def test_save_to_cache(self):
        self.assertTrue(self.cache.empty())

        self.cache.save(np.asarray([[[1, 2, 3],
                                    [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        1.0, 120.0, 1.)

        self.assertFalse(self.cache.empty())
        hist, bins = self.cache.get_histograms()
        self.assertArrays(hist, [[[1, 2, 3],
                                  [4, 5, 6]]])
        self.assertArrays(bins, [7, 8, 9])
        self.assertArrays(self.cache._discarded_good_frames,
                          np.asarray([30], dtype=np.int32))
        self.assertArrays(self.cache.get_discarded_raw_frames,
                          np.asarray([20], dtype=np.int32))
        self.assertArrays(self.cache.get_good_frames,
                          np.asarray([70], dtype=np.int32))
        self.assertArrays(self.cache.get_raw_frames,
                          np.asarray([80], dtype=np.int32))
        self.assertEqual(self.cache.get_resolution(), 1.)

    def test_clear_cache(self):
        self.assertTrue(self.cache.empty())

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        1.0, 120.0, 1.)

        self.assertFalse(self.cache.empty())

        self.cache.clear()
        self.assertTrue(self.cache.empty())
        with self.assertRaises(RuntimeError):
            self.cache.get_histograms()
        with self.assertRaises(RuntimeError):
            self.cache.get_discarded_raw_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_good_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_raw_frames
        with self.assertRaises(RuntimeError):
            self.cache.get_resolution()

    def test_set_too_many_filter_frames(self):
        self.assertTrue(self.cache.empty())

        with self.assertRaises(RuntimeError):
            self.cache.save(np.asarray([[[1, 2, 3],
                                         [4, 5, 6]]], dtype=np.int32),
                            np.asarray([7, 8, 9], dtype=np.double),
                            np.asarray([1, 2], dtype=np.int32),
                            np.asarray([1], dtype=np.int32),
                            1.0, 120.0, 1.0)

    def test_set_too_many_veto_frames(self):
        self.assertTrue(self.cache.empty())

        with self.assertRaises(RuntimeError):
            self.cache.save(np.asarray([[[1, 2, 3],
                                         [4, 5, 6]]], dtype=np.int32),
                            np.asarray([7, 8, 9], dtype=np.double),
                            np.asarray([1], dtype=np.int32),
                            np.asarray([1, 20], dtype=np.int32),
                            1., 120., 1.)

    def test_duration(self):

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        1, 120, 1.)
        self.assertAlmostEqual(self.cache.get_count_duration, 1.75, 3)

    def test_get_start_time_zero_no_offseet(self):

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        0, 120, 1.)
        expect = convert_date_for_NXS(self.date)
        self.assertEqual(convert_date_for_NXS(self.cache.get_start_time),
                         expect)

    def test_get_start_time_zero_offseet(self):

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        132, 220, 1.)
        expect = convert_date_for_NXS(datetime.datetime(2024, 11,
                                                        21, 8, 1, 12))
        self.assertEqual(convert_date_for_NXS(self.cache.get_start_time),
                         expect)

    def test_get_end_time(self):

        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        0, 220, 1.)
        expect = convert_date_for_NXS(datetime.datetime(2024, 11,
                                                        21, 8, 2, 40))
        self.assertEqual(convert_date_for_NXS(self.cache.get_end_time),
                         expect)

    def test_get_duration(self):
        self.cache.save(np.asarray([[[1, 2, 3],
                                     [4, 5, 6]]], dtype=np.int32),
                        np.asarray([7, 8, 9], dtype=np.double),
                        np.asarray([20], dtype=np.int32),
                        np.asarray([10], dtype=np.int32),
                        132, 220, 1.)
        self.assertEqual(self.cache.get_duration,
                         88)


if __name__ == '__main__':
    unittest.main()
