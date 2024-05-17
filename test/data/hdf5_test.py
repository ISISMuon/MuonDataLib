from MuonDataLib.data.hdf5 import HDF5
from MuonDataLib.test_helpers.nexus import NexusTestHelper

import h5py
import unittest
import os


FILENAME = 'hdf5_test.nxs'


class HDF5Test(NexusTestHelper):

    def test_save_str(self):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            hdf5.save_str('unit', 'test', group)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['data'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['unit'])
            self.assertString(group, 'unit', 'test')

        os.remove(FILENAME)

    def bad_str_value(self, value):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_str('unit', value, group)

        os.remove(FILENAME)

    def test_save_str_bad_value_int(self):
        self.bad_str_value(5)

    def test_save_str_bad_value_int_list(self):
        self.bad_str_value([5])

    def test_save_str_bad_value_float(self):
        self.bad_str_value(5.2)

    def test_save_str_bad_value_float_list(self):
        self.bad_str_value([5.2])

    def test_save_float(self):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            hdf5.save_float('mean', 2.35, group)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['data'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['mean'])
            self.assertArrays(group['mean'], [2.35])

        os.remove(FILENAME)

    def float_bad_value(self, value):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_float('mean', value, group)

        os.remove(FILENAME)

    def test_save_float_bad_value_string(self):
        self.float_bad_value('test')

    def test_save_float_bad_value_int(self):
        self.float_bad_value(2)

    def test_save_float_bad_value_int_list(self):
        self.float_bad_value([2])

    def test_save_float_bad_value_float_list(self):
        self.float_bad_value([2.3])

    def test_save_int(self):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            hdf5.save_int('version', 5, group)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['data'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['version'])
            self.assertArrays(group['version'], [5])

        os.remove(FILENAME)

    def int_bad_value(self, value):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_int('version', value, group)

        os.remove(FILENAME)

    def test_int_bad_value_string(self):
        self.int_bad_value('test')

    def test_int_bad_value_float(self):
        self.int_bad_value(1.2)

    def test_int_bad_value_list_int(self):
        self.int_bad_value([3])

    def test_int_bad_value_list_float(self):
        self.int_bad_value([1.2])

    def test_save_int_array(self):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            hdf5.save_int_array('count down',
                                [5, 4, 3, 2], group)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['data'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['count down'])
            self.assertArrays(group['count down'],
                              [5, 4, 3, 2])

        os.remove(FILENAME)

    def int_array_bad_value(self, value):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_int_array('count down', value, group)
        os.remove(FILENAME)

    def test_int_array_bad_value_string(self):
        self.int_array_bad_value('test')

    def test_int_array_bad_value_int(self):
        self.int_array_bad_value(1)

    def test_int_array_bad_value_float(self):
        self.int_array_bad_value(2.3)

    def test_int_array_bad_value_list_float(self):
        self.int_array_bad_value([2.3])

    def test_save_float_array(self):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            hdf5.save_float_array('stats', [0.018, 0.039, 0.015], group)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['data'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['stats'])
            self.assertArrays(group['stats'], [0.018, 0.039, 0.015])

        os.remove(FILENAME)

    def float_array_bad_value(self, value):
        hdf5 = HDF5()

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_float_array('stats', value, group)

        os.remove(FILENAME)

    def test_float_array_bad_value_string(self):
        self.float_array_bad_value('test')

    def test_float_array_bad_value_int(self):
        self.float_array_bad_value(1)

    def test_float_array_bad_value_float(self):
        self.float_array_bad_value(1.2)

    def test_float_array_bad_value_int_array(self):
        self.float_array_bad_value([1])

    def test_save_counts_array(self):
        hdf5 = HDF5()
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p):
            counts.append([])
            for i in range(N_hist):
                counts[p].append([j for j in range(N_x)])

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            hdf5.save_counts_array('counts', N_p, N_hist, N_x, counts, group)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['data'])
            group = file[keys[0]]

            keys = self.compare_keys(group, ['counts'])
            self.assertArrays(group['counts'], counts)

        os.remove(FILENAME)

    def test_save_counts_array_bad_period_length(self):
        hdf5 = HDF5()
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p + 1):
            counts.append([])
            for i in range(N_hist):
                counts[p].append([j for j in range(N_x)])

        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_counts_array('counts',
                                       N_p,
                                       N_hist,
                                       N_x,
                                       counts,
                                       group)

        os.remove(FILENAME)

    def counts_bad_value(self, N_p, N_hist, N_x, counts):
        hdf5 = HDF5()
        with h5py.File(FILENAME, 'w') as file:
            group = file.require_group('data')
            with self.assertRaises(ValueError):
                hdf5.save_counts_array('counts',
                                       N_p,
                                       N_hist,
                                       N_x,
                                       counts,
                                       group)

        os.remove(FILENAME)

    def test_save_counts_array_bad_spec_length(self):
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p):
            counts.append([])
            for i in range(N_hist - 1):
                counts[p].append([j for j in range(N_x + 1)])
        self.counts_bad_value(N_p, N_hist, N_x, counts)

    def test_save_counts_array_bad_x_length(self):
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p):
            counts.append([])
            for i in range(N_hist):
                counts[p].append([j for j in range(N_x + 1)])

        self.counts_bad_value(N_p, N_hist, N_x, counts)

    def test_save_counts_array_bad_value_str(self):
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p):
            counts.append([])
            for i in range(N_hist):
                counts[p].append(['count' for j in range(N_x)])

        self.counts_bad_value(N_p, N_hist, N_x, counts)

    def test_save_counts_array_bad_value_float(self):
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p):
            counts.append([])
            for i in range(N_hist):
                counts[p].append([1.2 for j in range(N_x)])

        self.counts_bad_value(N_p, N_hist, N_x, counts)

    def test_save_counts_array_bad_value_list(self):
        counts = []
        N_p = 2
        N_hist = 3
        N_x = 4

        for p in range(N_p):
            counts.append([])
            for i in range(N_hist):
                counts[p].append([[j] for j in range(N_x)])

        self.counts_bad_value(N_p, N_hist, N_x, counts)


if __name__ == '__main__':
    unittest.main()
