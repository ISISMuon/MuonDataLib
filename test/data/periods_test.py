from MuonDataLib.data.periods import (Periods,
                                      read_periods_from_histogram)

from MuonDataLib.test_helpers.nexus import NexusTestHelper
import h5py
import unittest
import os


FILENAME = 'periods_test.nxs'


def create_single_period_data():
    return Periods(1, 'period 1', [1], [500], [1000], [1], [1.23], [2])


def create_multiperiod_data():
    return Periods(2, 'period 1; period 2', [1, 2], [500, 400],
                   [1000, 500], [1, 0], [1.23, 4.56], [42, 42])


class PeriodsTest(NexusTestHelper):

    def test_periods_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        period = create_single_period_data()

        self.assertEqual(period._dict['number'], 1)
        self.assertEqual(period._dict['labels'], 'period 1')
        self.assertArrays(period._dict['type'], [1])
        self.assertArrays(period._dict['requested'], [500])
        self.assertArrays(period._dict['raw'], [1000])
        self.assertArrays(period._dict['output'], [1])
        self.assertArrays(period._dict['sequences'], [2])
        self.assertArrays(period._dict['counts'], [1.23])

    def test_periods_object_saves_correct_info_single_period(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        periods = create_single_period_data()

        with h5py.File(FILENAME, 'w') as file:
            periods.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            keys = self.compare_keys(group, ['periods'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXperiod')

            self.assertEqual(group['number'][0], 1)
            self.assertString(group, 'labels', 'period 1')
            self.assertArrays(group['type'], [1])
            self.assertArrays(group['frames_requested'], [500])
            self.assertArrays(group['raw_frames'], [1000])
            self.assertArrays(group['output'], [1])
            self.assertArrays(group['sequences'], [2])
            self.assertArrays(group['total_counts'], [1.23])

        os.remove(FILENAME)

    def test_load_periods_gets_correct_info_single_period(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        period = create_single_period_data()

        with h5py.File(FILENAME, 'w') as file:
            period.save_nxs2(file)
        del period

        with h5py.File(FILENAME, 'r') as file:
            load_period = read_periods_from_histogram(file)

        self.assertEqual(load_period._dict['number'], 1)
        self.assertEqual(load_period._dict['labels'], 'period 1')
        self.assertArrays(load_period._dict['type'], [1])
        self.assertArrays(load_period._dict['requested'], [500])
        self.assertArrays(load_period._dict['raw'], [1000])
        self.assertArrays(load_period._dict['output'], [1])
        self.assertArrays(load_period._dict['sequences'], [2])
        self.assertArrays(load_period._dict['counts'], [1.23])

        os.remove(FILENAME)

    def test_periods_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        period = create_multiperiod_data()

        self.assertEqual(period._dict['number'], 2)
        self.assertEqual(period._dict['labels'], 'period 1; period 2')
        self.assertArrays(period._dict['type'], [1, 2])
        self.assertArrays(period._dict['requested'], [500, 400])
        self.assertArrays(period._dict['raw'], [1000, 500])
        self.assertArrays(period._dict['output'], [1, 0])
        self.assertArrays(period._dict['sequences'], [42, 42])
        self.assertArrays(period._dict['counts'], [1.23, 4.56])

    def test_periods_object_saves_correct_info_multiperiod(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        period = create_multiperiod_data()

        with h5py.File(FILENAME, 'w') as file:
            period.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]
            keys = self.compare_keys(group, ['periods'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXperiod')

            self.assertEqual(group['number'][0], 2)
            self.assertEqual(group['labels'][0].decode(), 'period 1; period 2')
            self.assertArrays(group['type'], [1, 2])
            self.assertArrays(group['frames_requested'], [500, 400])
            self.assertArrays(group['raw_frames'], [1000, 500])
            self.assertArrays(group['output'], [1, 0])
            self.assertArrays(group['sequences'], [42, 42])
            self.assertArrays(group['total_counts'], [1.23, 4.56])

        os.remove(FILENAME)

    def test_load_detector1_gets_correct_info_multiperiod(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        period = create_multiperiod_data()

        with h5py.File(FILENAME, 'w') as file:
            period.save_nxs2(file)
        del period

        with h5py.File(FILENAME, 'r') as file:
            load_period = read_periods_from_histogram(file)

        self.assertEqual(load_period._dict['number'], 2)
        self.assertEqual(load_period._dict['labels'], 'period 1; period 2')
        self.assertArrays(load_period._dict['type'], [1, 2])
        self.assertArrays(load_period._dict['requested'], [500, 400])
        self.assertArrays(load_period._dict['raw'], [1000, 500])
        self.assertArrays(load_period._dict['output'], [1, 0])
        self.assertArrays(load_period._dict['sequences'], [42, 42])
        self.assertArrays(load_period._dict['counts'], [1.23, 4.56])

        os.remove(FILENAME)


if __name__ == '__main__':
    unittest.main()
