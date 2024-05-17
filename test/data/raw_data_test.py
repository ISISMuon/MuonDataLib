from MuonDataLib.data.raw_data import (RawData,
                                       read_raw_data_from_histogram)

from MuonDataLib.test_helpers.nexus import NexusTestHelper
import h5py
import unittest
import os
import datetime


FILENAME = 'raw_data_test.nxs'


def create_data():
    start = datetime.datetime(2018, 12, 24, 13, 32, 1)
    end = datetime.datetime(2018, 12, 24, 18, 11, 52)

    return (RawData(10, 1, 'pulsed', 'python', 'raw data test',
                    'testing', 42, 1024.0, 51, start, end, '19'),
            start, end)


class RawDataTest(NexusTestHelper):

    def test_raw_data_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        raw, start, end = create_data()

        self.assertEqual(raw._dict['good_frames'], 10)
        self.assertEqual(raw._dict['IDF'], 1)
        self.assertEqual(raw._dict['def'], 'pulsed')
        self.assertEqual(raw._dict['inst'], 'python')
        self.assertEqual(raw._dict['title'], 'raw data test')
        self.assertEqual(raw._dict['notes'], 'testing')
        self.assertEqual(raw._dict['run_number'], 42)
        self.assertAlmostEqual(raw._dict['duration'], 1024.0, 3)
        self.assertEqual(raw._dict['raw_frames'], 51)
        self.assertEqual(raw._dict['start'], start)
        self.assertEqual(raw._dict['end'], end)

    def test_raw_data_object_saves_correct_info(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        raw, _, _ = create_data()

        with h5py.File(FILENAME, 'w') as file:
            raw.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXentry')

            keys = self.compare_keys(group, ['good_frames',
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
            self.assertArrays(group['duration'], [1024.0])
            self.assertArrays(group['raw_frames'], [51])
            self.assertString(group, 'start_time', '2018-12-24T13:32:01')
            self.assertString(group, 'end_time', '2018-12-24T18:11:52')

            group = group['instrument']
            self.compare_keys(group, ['name'])
            self.assertString(group, 'name', 'python')

        os.remove(FILENAME)

    def test_load_raw_data_gets_correct_info(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        raw, start, end = create_data()

        with h5py.File(FILENAME, 'w') as file:
            raw.save_nxs2(file)

        del raw

        with h5py.File(FILENAME, 'r') as file:
            load_raw = read_raw_data_from_histogram(file)

        self.assertEqual(load_raw._dict['good_frames'], 10)
        self.assertEqual(load_raw._dict['IDF'], 1)
        self.assertEqual(load_raw._dict['def'], 'pulsed')
        self.assertEqual(load_raw._dict['inst'], 'python')
        self.assertEqual(load_raw._dict['title'], 'raw data test')
        self.assertEqual(load_raw._dict['notes'], 'testing')
        self.assertEqual(load_raw._dict['run_number'], 42)
        self.assertAlmostEqual(load_raw._dict['duration'], 1024.0, 3)
        self.assertEqual(load_raw._dict['raw_frames'], 51)
        self.assertEqual(load_raw._dict['start'], start)
        self.assertEqual(load_raw._dict['end'], end)

        os.remove(FILENAME)


if __name__ == '__main__':
    unittest.main()
