from MuonDataLib.data.sample import (Sample,
                                     read_sample_from_histogram)

from MuonDataLib.test_helpers.nexus import NexusTestHelper
import h5py
import unittest
import os


FILENAME = 'sample_test.nxs'


def create_data():
    return Sample('ISIS2', 23.1, 12.2, 13.3, 5.1, 312.6, 'Si')


class SampleTest(NexusTestHelper):

    def test_sample_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        sample = create_data()

        self.assertEqual(sample._dict['ID'], 'ISIS2')
        self.assertEqual(sample._dict['name'], 'Si')
        self.assertAlmostEqual(sample._dict['thickness'], 23.1, 3)
        self.assertAlmostEqual(sample._dict['height'], 12.2, 3)
        self.assertAlmostEqual(sample._dict['width'], 13.3, 3)
        self.assertAlmostEqual(sample._dict['B_field'], 5.1, 3)
        self.assertAlmostEqual(sample._dict['Temp'], 312.6, 3)

    def test_sample_object_saves_correct_info(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        sample = create_data()

        with h5py.File(FILENAME, 'w') as file:
            sample.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['sample'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXsample')

            keys = self.compare_keys(group, ['id',
                                             'name',
                                             'thickness',
                                             'height',
                                             'width',
                                             'magnetic_field',
                                             'temperature'])
            self.assertString(group, 'id', 'ISIS2')
            self.assertString(group, 'name', 'Si')
            self.assertArrays(group['thickness'], [23.1])
            self.assertArrays(group['height'], [12.2])
            self.assertArrays(group['width'], [13.3])
            self.assertArrays(group['magnetic_field'], [5.1])
            self.assertArrays(group['temperature'], [312.6])
        os.remove(FILENAME)

    def test_load_sample_gets_correct_info(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        sample = create_data()

        with h5py.File(FILENAME, 'w') as file:
            sample.save_nxs2(file)

        del sample

        with h5py.File(FILENAME, 'r') as file:
            load_sample = read_sample_from_histogram(file)

        self.assertEqual(load_sample._dict['ID'], 'ISIS2')
        self.assertEqual(load_sample._dict['name'], 'Si')
        self.assertAlmostEqual(load_sample._dict['thickness'], 23.1, 3)
        self.assertAlmostEqual(load_sample._dict['height'], 12.2, 3)
        self.assertAlmostEqual(load_sample._dict['width'], 13.3, 3)
        self.assertAlmostEqual(load_sample._dict['B_field'], 5.1, 3)
        self.assertAlmostEqual(load_sample._dict['Temp'], 312.6, 3)

        os.remove(FILENAME)


if __name__ == '__main__':
    unittest.main()
