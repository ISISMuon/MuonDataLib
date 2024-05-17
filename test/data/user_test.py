from MuonDataLib.data.user import (User,
                                   read_user_from_histogram)

from MuonDataLib.test_helpers.nexus import NexusTestHelper
import h5py
import unittest
import os


FILENAME = 'user_test.nxs'


class UserTest(NexusTestHelper):

    def test_user_object_stores_correct_info(self):
        """
        Check the class stores data correctly
        """
        user = User('Unit Test', 'Python')

        self.assertEqual(user._dict['name'], 'Unit Test')
        self.assertEqual(user._dict['affiliation'], 'Python')

    def test_user_object_saves_correct_info(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        user = User('Unit Test', 'Python')

        with h5py.File(FILENAME, 'w') as file:
            user.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])

            group = file[keys[0]]

            keys = self.compare_keys(group, ['user_1'])
            group = group[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXuser')

            keys = self.compare_keys(group, ['name', 'affiliation'])

            self.assertString(group, 'name', 'Unit Test')
            self.assertString(group, 'affiliation', 'Python')

        os.remove(FILENAME)

    def test_load_user_gets_correct_info(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        user = User('Unit Test', 'Python')

        with h5py.File(FILENAME, 'w') as file:
            user.save_nxs2(file)
        del user

        with h5py.File(FILENAME, 'r') as file:
            load_user = read_user_from_histogram(file)

        self.assertEqual(load_user._dict['name'], 'Unit Test')
        self.assertEqual(load_user._dict['affiliation'], 'Python')

        os.remove(FILENAME)


if __name__ == '__main__':
    unittest.main()
