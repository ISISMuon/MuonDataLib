from MuonDataLib.data.raw_data import (_RawData,
                                       RawData,
                                       EventsRawData)

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.raw_data import RawDataTestTemplate
from MuonDataLib.cython_ext.events_cache import EventsCache
import unittest
import numpy as np
import datetime


class _RawDataTest(RawDataTestTemplate, TestHelper):

    def create_data(self):
        args = super().create_data()
        self.good_frames = args[0]
        self.raw_frames = args[8]

        return (_RawData(args[1], args[2],
                         args[3], args[4],
                         args[5], args[6],
                         args[7], args[9],
                         args[10], args[11]),
                args[9], args[10])

    def save(self, raw, file):
        raw.save_nxs2(file, self.good_frames,
                      self.raw_frames)

    def setUp(self):
        self.filename = '_raw_data.nxs'


class RawDataTest(RawDataTestTemplate, TestHelper):

    def create_data(self):
        args = super().create_data()
        return RawData(*args), args[9], args[10]

    def save(self, raw, file):
        raw.save_nxs2(file)

    def setUp(self):
        self.filename = '_raw_data.nxs'

    def test_raw_data_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        super().test_raw_data_object_stores_correct_info()

        self.assertEqual(self.raw._dict['good_frames'], 10)
        self.assertEqual(self.raw._dict['raw_frames'], 51)


class EventsRawDataTest(RawDataTestTemplate, TestHelper):

    def create_data(self):
        args = super().create_data()
        date = datetime.datetime(2024, 11, 21, 7, 59, 0)
        cache = EventsCache(date, np.asarray([args[8]], dtype=np.int32))
        raw = EventsRawData(cache,
                            args[1], args[2],
                            args[3], args[4],
                            args[5], args[6],
                            args[7], args[9],
                            args[10], args[11])
        counts = np.asarray([[[1]]], dtype=np.int32)
        bins = np.asarray([1, 2], dtype=np.double)
        cache.save(counts, bins,
                   np.asarray([0], dtype=np.int32),
                   np.asarray([41], dtype=np.int32))
        return raw, args[9], args[10]

    def save(self, raw, file):
        raw.save_nxs2(file)

    def setUp(self):
        self.filename = 'events_raw_data.nxs'

    def test_raw_data_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        super().test_raw_data_object_stores_correct_info()

        good = np.asarray(self.raw._cache.get_good_frames)
        self.assertEqual(good, 10)
        total = np.asarray(self.raw._cache.get_raw_frames)
        self.assertEqual(total, 51)


if __name__ == '__main__':
    unittest.main()
