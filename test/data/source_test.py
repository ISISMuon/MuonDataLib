from MuonDataLib.data.source import (Source,
                                     read_source_from_histogram)

from MuonDataLib.test_helpers.nexus import NexusTestHelper
import h5py
import unittest
import os


FILENAME = 'source_test.nxs'


def create_data():
    return Source('python', 'muon', 'pulsed')


class SourceTest(NexusTestHelper):

    def test_source_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        source = create_data()

        self.assertEqual(source._dict['name'], 'python')
        self.assertEqual(source._dict['probe'], 'muon')
        self.assertEqual(source._dict['type'], 'pulsed')

    def test_source_object_saves_correct_info(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        source = create_data()

        with h5py.File(FILENAME, 'w') as file:
            source.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['instrument'])
            group = group[keys[0]]

            keys = self.compare_keys(group, ['source'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXsource')

            keys = self.compare_keys(group, ['name',
                                             'type',
                                             'probe'])

            self.assertString(group, 'name', 'python')
            self.assertString(group, 'probe', 'muon')
            self.assertString(group, 'type', 'pulsed')

        os.remove(FILENAME)

    def test_load_source_gets_correct_info(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        source = create_data()

        with h5py.File(FILENAME, 'w') as file:
            source.save_nxs2(file)

        del source

        with h5py.File(FILENAME, 'r') as file:
            load_source = read_source_from_histogram(file)

        self.assertEqual(load_source._dict['name'], 'python')
        self.assertEqual(load_source._dict['probe'], 'muon')
        self.assertEqual(load_source._dict['type'], 'pulsed')

        os.remove(FILENAME)


if __name__ == '__main__':
    unittest.main()
