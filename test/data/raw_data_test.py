from MuonDataLib.data.raw_data import (_RawData,
                                       RawData,
                                       EventsRawData)

from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.raw_data import RawDataTestTemplate
from MuonDataLib.cython_ext.events_cache import EventsCache
import unittest
import numpy as np
import datetime
import h5py
import os


class _RawDataTest(RawDataTestTemplate, TestHelper):

    def create_data(self):
        args = super().create_data()
        self.good_frames = args[0]
        self.raw_frames = args[8]
        self.start = args[9]
        self.end = args[10]
        self.duration = args[7]

        return (_RawData(args[1], args[2],
                         args[3], args[4],
                         args[5], args[6],
                         args[11]),
                args[9], args[10])

    def save(self, raw, file):
        raw.save_nxs2(file, self.good_frames,
                      self.raw_frames,
                      self.start, self.end,
                      self.duration)

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
        date = args[9]
        cache = EventsCache(date, np.asarray([args[8]], dtype=np.int32))
        raw = EventsRawData(cache,
                            args[1], args[2],
                            args[3], args[4],
                            args[5], args[6],
                            args[11])
        counts = np.asarray([[[1]]], dtype=np.int32)
        bins = np.asarray([1, 2], dtype=np.double)
        cache.save(counts, bins,
                   np.asarray([0], dtype=np.int32),
                   np.asarray([41], dtype=np.int32),
                   0, (args[10] - args[9]).total_seconds(),
                   0.016, 1e6)
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
        self.assertEqual(self.raw._cache.get_start_time,
                         datetime.datetime(2018, 12, 24,
                                           13, 32, 1))
        self.assertEqual(self.raw._cache.get_end_time,
                         datetime.datetime(2018, 12, 24,
                                           18, 11, 52))

    def test_raw_data_object_saves_correct_info(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        raw, _, _ = self.create_data()

        with h5py.File(self.filename, 'w') as file:
            self.save(raw, file)

        with h5py.File(self.filename, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXentry')

            keys = self.compare_keys(group, ['good_frames',
                                             'count_duration',
                                             'discarded_raw_frames',
                                             'IDF_version',
                                             'definition',
                                             'name',
                                             'title',
                                             'notes',
                                             'run_number',
                                             'duration',
                                             'raw_frames',
                                             'start_time',
                                             'end_time',
                                             'experiment_identifier',
                                             'instrument'])

            self.assertArrays(group['good_frames'], [10])
            self.assertArrays(group['IDF_version'], [1])
            self.assertString(group, 'definition', 'pulsed')
            self.assertString(group, 'name', 'python')
            self.assertString(group, 'title', 'raw data test')
            self.assertString(group, 'notes', 'testing')
            self.assertArrays(group['run_number'], [42])
            self.assertArrays(group['duration'], [16791.0])
            self.assertArrays(group['raw_frames'], [51])
            self.assertString(group, 'start_time', '2018-12-24T13:32:01')
            self.assertString(group, 'end_time', '2018-12-24T18:11:52')

            group = group['instrument']
            self.compare_keys(group, ['name'])
            self.assertString(group, 'name', 'python')

        os.remove(self.filename)


if __name__ == '__main__':
    unittest.main()
