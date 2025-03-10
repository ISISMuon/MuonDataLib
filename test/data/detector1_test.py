from MuonDataLib.data.detector1 import (_Detector_1,
                                        Detector_1,
                                        EventsDetector_1)
from MuonDataLib.cython_ext.events_cache import EventsCache
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.detector1 import Det1TestTemplate
import unittest
import numpy as np
import datetime


class _Detector1Test(Det1TestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        self.raw = args[1]
        self.counts = args[3]
        return _Detector_1(args[0], args[2], args[4],
                           args[5], args[6], args[7])

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        self.raw = args[1]
        self.counts = args[3]
        return _Detector_1(args[0], args[2], args[4],
                           args[5], args[6], args[7])

    def setUp(self):
        self.filename = '_detector_1.nxs'

    def save(self, det, file):
        det.save_nxs2(file, self.raw,
                      self.counts,
                      len(self.counts[0][0]),
                      len(self.counts[0]),
                      len(self.counts))


class Detector1Test(Det1TestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        return Detector_1(*args)

    def create_multiperiod_data(self):
        args = super().create_multiperiod_data()
        return Detector_1(*args)

    def setUp(self):
        self.filename = 'detector_1.nxs'

    def save(self, det, file):
        det.save_nxs2(file)

    def test_detector1_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        super().test_detector1_object_stores_correct_info_single_period()

        self.assertArrays(self.det._dict['raw_time'], [1, 2, 3])
        self.assertArrays(self.det._dict['counts'], [
                                                     [[1, 1, 1],
                                                      [2, 2, 2],
                                                      [3, 3, 3],
                                                      [4, 4, 4]]])
        self.assertEqual(self.det.N_x, 3)
        self.assertEqual(self.det.N_hist, 4)
        self.assertEqual(self.det.N_periods, 1)


class EventsDetector1Test(Det1TestTemplate, TestHelper):

    def create_single_period_data(self):
        args = super().create_single_period_data()
        bins = np.asarray(args[1], dtype=np.double)
        counts = np.asarray(args[3], dtype=np.int32)
        date = datetime.datetime(2024, 12, 11, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))
        events = EventsDetector_1(cache, args[0],
                                  args[2], args[4],
                                  args[5], args[6],
                                  args[7])
        cache.save(counts, bins, np.asarray([1], dtype=np.int32),
                   np.asarray([0], dtype=np.int32),
                   0.0, 100.0, resolution=0.016, N_events=1e6)
        return events

    def create_multiperiod_data(self):
        # this is her to be updated when multiperiod works
        args = super().create_multiperiod_data()
        bins = np.asarray(args[1], dtype=np.double)
        counts = np.asarray(args[3], dtype=np.int32)
        date = datetime.datetime(2024, 12, 11, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))
        events = EventsDetector_1(cache, args[0],
                                  args[2], args[4],
                                  args[5], args[6],
                                  args[7])
        cache.save(counts, bins,
                   np.asarray([1], dtype=np.int32),
                   np.asarray([0], dtype=np.int32),
                   0.0, 100.0, resolution=0.016, N_events=1e6)
        return events

    def create_single_period_data_custom_resolution(self):
        args = super().create_single_period_data()
        bins = np.asarray(args[1], dtype=np.double)
        counts = np.asarray(args[3], dtype=np.int32)
        date = datetime.datetime(2024, 12, 11, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))

        # change the time stamps so they stay in the same bin
        conversion = 0.01/0.016

        events = EventsDetector_1(cache, args[0],
                                  args[2], args[4],
                                  conversion * args[5],
                                  conversion * args[6],
                                  conversion * args[7])
        cache.save(counts, bins, np.asarray([1], dtype=np.int32),
                   np.asarray([0], dtype=np.int32),
                   0.0, 100.0, resolution=0.01, N_events=1e6)
        return events

    def create_multiperiod_data_custom_resolution(self):
        # this is her to be updated when multiperiod works
        args = super().create_multiperiod_data()
        bins = np.asarray(args[1], dtype=np.double)
        counts = np.asarray(args[3], dtype=np.int32)
        date = datetime.datetime(2024, 12, 11, 7, 59, 0)
        cache = EventsCache(date, np.asarray([100], dtype=np.int32))

        # change the time stamps so they stay in the same bin
        conversion = 0.01/0.016

        events = EventsDetector_1(cache, args[0],
                                  args[2], args[4],
                                  conversion * args[5],
                                  conversion * args[6],
                                  conversion * args[7])
        cache.save(counts, bins,
                   np.asarray([1], dtype=np.int32),
                   np.asarray([0], dtype=np.int32),
                   0.0, 100.0, resolution=0.01, N_events=1e6)
        return events

    def setUp(self):
        self.filename = 'events_detector_1.nxs'

    def save(self, det, file):
        det.save_nxs2(file)

    def test_detector1_object_saves_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        super().test_detector1_object_stores_correct_info_single_period()

        counts, bins = self.det._cache.get_histograms()

        self.assertArrays(bins, [1, 2, 3])
        self.assertArrays(counts, [
                                   [[1, 1, 1],
                                    [2, 2, 2],
                                    [3, 3, 3],
                                    [4, 4, 4]]])
        self.assertEqual(len(counts[0][0]), 3)
        self.assertEqual(len(counts[0]), 4)
        self.assertEqual(len(counts), 1)

    def test_detector1_object_saves_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        super().test_detector1_object_stores_correct_info_multiperiod()

        counts, bins = self.det._cache.get_histograms()
        self.assertArrays(bins, [1., 2., 3.])
        self.assertArrays(counts, [
                                   [[1, 1, 1], [1, 1, 1]],
                                   [[2, 2, 2], [2, 2, 2]],
                                   [[3, 3, 3], [3, 3, 3]]])

        self.assertEqual(len(counts[0][0]), 3)
        self.assertEqual(len(counts[0]), 2)
        self.assertEqual(len(counts), 3)

    def test_detector1_object_saves_correct_info_single_period_res(self):
        """
        Check the class stores data correctly
        """
        det = self.create_single_period_data_custom_resolution()
        res = self._detector1_object_saves_correct_info_single_period(det)
        self.assertEqual(res, 10000)
        counts, bins = det._cache.get_histograms()

        self.assertArrays(bins, [1, 2, 3])
        self.assertArrays(counts, [
                                   [[1, 1, 1],
                                    [2, 2, 2],
                                    [3, 3, 3],
                                    [4, 4, 4]]])
        self.assertEqual(len(counts[0][0]), 3)
        self.assertEqual(len(counts[0]), 4)
        self.assertEqual(len(counts), 1)

    def test_detector1_object_saves_correct_info_multiperiod_res(self):
        """
        Check the class stores data correctly
        """
        det = self.create_multiperiod_data_custom_resolution()
        res = self._detector1_object_saves_correct_info_multiperiod(det)
        self.assertEqual(res, 10000)
        counts, bins = det._cache.get_histograms()
        self.assertArrays(bins, [1., 2., 3.])
        self.assertArrays(counts, [
                                   [[1, 1, 1], [1, 1, 1]],
                                   [[2, 2, 2], [2, 2, 2]],
                                   [[3, 3, 3], [3, 3, 3]]])

        self.assertEqual(len(counts[0][0]), 3)
        self.assertEqual(len(counts[0]), 2)
        self.assertEqual(len(counts), 3)

    def test_fist_good_middle_of_bin(self):
        det = self.create_multiperiod_data_custom_resolution()
        result = det.get_first_good_bin(0.042)
        self.assertEqual(result, 5)

    def test_fist_good_start_of_bin(self):
        det = self.create_multiperiod_data_custom_resolution()
        result = det.get_first_good_bin(0.04)
        self.assertEqual(result, 4)

    def test_last_good_middle_of_bin(self):
        det = self.create_multiperiod_data_custom_resolution()
        result = det.get_last_good_bin(0.042)
        self.assertEqual(result, 3)

    def test_last_good_start_of_bin(self):
        det = self.create_multiperiod_data_custom_resolution()
        result = det.get_last_good_bin(0.04)
        self.assertEqual(result, 3)

    def test_t0_middle_of_bin(self):
        det = self.create_multiperiod_data_custom_resolution()
        result = det.get_time_zero_bin(0.042)
        self.assertEqual(result, 4)

    def test_t0_start_of_bin(self):
        det = self.create_multiperiod_data_custom_resolution()
        result = det.get_time_zero_bin(0.04)
        self.assertEqual(result, 4)


if __name__ == '__main__':
    unittest.main()
