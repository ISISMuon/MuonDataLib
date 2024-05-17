from MuonDataLib.data.detector1 import (Detector_1,
                                        read_detector1_from_histogram)

from MuonDataLib.test_helpers.nexus import NexusTestHelper
import h5py
import os
import unittest
import numpy as np


FILENAME = 'detector1_test.nxs'


def create_single_period_data():
    x = [1., 2., 3.]
    # counts: shape(periods, spec, x)
    counts = []
    for p in range(1):
        counts.append([])
        for j in range(4):
            tmp = (((j + 1) * np.ones(len(x))))
            counts[p].append([int(x) for x in tmp])

    return Detector_1(1, x, [4, 5, 6, 7], counts, 'python', 3, 4, 42)


def create_multiperiod_data():
    x = [1., 2., 3.]
    # counts: shape(periods, spec, x)
    counts = []
    for p in range(3):
        counts.append([])
        for j in range(2):
            tmp = (((p + 1) * np.ones(len(x))))
            counts[p].append([int(x) for x in tmp])

    return Detector_1(1, x, [4, 5], counts, 'python', 3, 4, 42)


class Detector1Test(NexusTestHelper):

    def test_detector1_object_stores_correct_info_single_period(self):
        """
        Check the class stores data correctly
        """
        det = create_single_period_data()

        self.assertEqual(det._dict['resolution'], 1)
        self.assertArrays(det._dict['raw_time'], [1, 2, 3])
        self.assertArrays(det._dict['spectrum_index'], [4, 5, 6, 7])
        self.assertEqual(det._dict['inst'], 'python')
        self.assertEqual(det._dict['time_zero'], 3)
        self.assertEqual(det._dict['first_good'], 4)
        self.assertEqual(det._dict['last_good'], 42)
        self.assertArrays(det._dict['counts'], [
                                                [[1, 1, 1],
                                                 [2, 2, 2],
                                                 [3, 3, 3],
                                                 [4, 4, 4]]])
        self.assertEqual(det.N_x, 3)
        self.assertEqual(det.N_hist, 4)
        self.assertEqual(det.N_periods, 1)

    def test_detector1_object_saves_correct_info_single_period(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        det = create_single_period_data()

        with h5py.File(FILENAME, 'w') as file:
            det.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            inst = file[keys[0]]

            keys = self.compare_keys(inst, ['instrument'])
            inst = inst[keys[0]]
            self.assertEqual(inst.attrs['NX_class'], 'NXinstrument')

            keys = self.compare_keys(inst, ['detector_1'])
            group = inst[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXdetector')

            keys = self.compare_keys(group, ['resolution',
                                             'raw_time',
                                             'spectrum_index',
                                             'counts',
                                             ])

            # check values
            self.assertEqual(group['resolution'][0], 1e6)
            self.assertArrays(group['raw_time'][:], [1., 2., 3.])
            self.assertArrays(group['spectrum_index'][:], [4, 5, 6, 7])
            self.assertArrays(group['counts'][:], [
                                                   [[1, 1, 1],
                                                    [2, 2, 2],
                                                    [3, 3, 3],
                                                    [4, 4, 4]]])

            # check attributes
            tmp = group['resolution']
            print(tmp.attrs['units'])
            self.assertEqual(tmp.attrs['units'].decode(), "picoseconds")

            tmp = group['raw_time']
            self.assertEqual(tmp.attrs['units'].decode(), 'microseconds')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'time')

            tmp = group['counts']
            self.assertEqual(tmp.attrs['axes'].decode(),
                             '[period index, spectrum index, raw time bin]')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'python')
            self.assertEqual(tmp.attrs['t0_bin'], 3)
            self.assertEqual(tmp.attrs['first_good_bin'], 4)
            self.assertEqual(tmp.attrs['last_good_bin'], 42)
        os.remove(FILENAME)

    def test_load_detector1_gets_correct_info_single_period(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        det = create_single_period_data()

        with h5py.File(FILENAME, 'w') as file:
            det.save_nxs2(file)
        del det

        with h5py.File(FILENAME, 'r') as file:
            load_det = read_detector1_from_histogram(file)

        self.assertEqual(load_det._dict['resolution'], 1)
        self.assertArrays(load_det._dict['raw_time'], [1, 2, 3])
        self.assertArrays(load_det._dict['spectrum_index'], [4, 5, 6, 7])
        self.assertEqual(load_det._dict['inst'], 'python')
        self.assertEqual(load_det._dict['time_zero'], 3)
        self.assertEqual(load_det._dict['first_good'], 4)
        self.assertEqual(load_det._dict['last_good'], 42)
        self.assertArrays(load_det._dict['counts'], [
                                                     [[1, 1, 1],
                                                      [2, 2, 2],
                                                      [3, 3, 3],
                                                      [4, 4, 4]]])
        self.assertEqual(load_det.N_x, 3)
        self.assertEqual(load_det.N_hist, 4)
        self.assertEqual(load_det.N_periods, 1)

        os.remove(FILENAME)

    def test_detector1_object_stores_correct_info_multiperiod(self):
        """
        Check the class stores data correctly
        """
        det = create_multiperiod_data()

        self.assertEqual(det._dict['resolution'], 1)
        self.assertArrays(det._dict['raw_time'], [1., 2., 3.])
        self.assertArrays(det._dict['spectrum_index'], [4, 5])
        self.assertEqual(det._dict['inst'], 'python')
        self.assertEqual(det._dict['time_zero'], 3)
        self.assertEqual(det._dict['first_good'], 4)
        self.assertEqual(det._dict['last_good'], 42)
        print(det._dict['counts'])
        self.assertArrays(det._dict['counts'], [
                                                [[1, 1, 1], [1, 1, 1]],
                                                [[2, 2, 2], [2, 2, 2]],
                                                [[3, 3, 3], [3, 3, 3]]])

        self.assertEqual(det.N_x, 3)
        self.assertEqual(det.N_hist, 2)
        self.assertEqual(det.N_periods, 3)

    def test_detector1_object_saves_correct_info_multiperiod(self):
        """
        Test that the class can save to a nexus file
        correctly
        """
        det = create_multiperiod_data()

        with h5py.File(FILENAME, 'w') as file:
            det.save_nxs2(file)

        with h5py.File(FILENAME, 'r') as file:
            keys = self.compare_keys(file, ['raw_data_1'])
            inst = file[keys[0]]

            keys = self.compare_keys(inst, ['instrument'])
            inst = inst[keys[0]]
            self.assertEqual(inst.attrs['NX_class'], 'NXinstrument')

            keys = self.compare_keys(inst, ['detector_1'])
            group = inst[keys[0]]
            self.assertEqual(group.attrs['NX_class'], 'NXdetector')

            keys = self.compare_keys(group, ['resolution',
                                             'raw_time',
                                             'spectrum_index',
                                             'counts',
                                             ])

            # check values
            self.assertEqual(group['resolution'][0], 1e6)
            self.assertArrays(group['raw_time'][:], [1., 2., 3.])
            self.assertArrays(group['spectrum_index'][:], [4, 5])
            self.assertArrays(group['counts'][:], [
                                                   [[1, 1, 1], [1, 1, 1]],
                                                   [[2, 2, 2], [2, 2, 2]],
                                                   [[3, 3, 3], [3, 3, 3]]])

            # check attributes
            tmp = group['resolution']
            print(tmp.attrs['units'])
            self.assertEqual(tmp.attrs['units'].decode(), "picoseconds")

            tmp = group['raw_time']
            self.assertEqual(tmp.attrs['units'].decode(), 'microseconds')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'time')

            tmp = group['counts']
            self.assertEqual(tmp.attrs['axes'].decode(),
                             '[period index, spectrum index, raw time bin]')
            self.assertEqual(tmp.attrs['long_name'].decode(), 'python')
            self.assertEqual(tmp.attrs['t0_bin'], 3)
            self.assertEqual(tmp.attrs['first_good_bin'], 4)
            self.assertEqual(tmp.attrs['last_good_bin'], 42)
        os.remove(FILENAME)

    def test_load_detector1_gets_correct_info_multiperiod(self):
        """
        Check load method gets the correct information.
        The above tests prove that the information
        stored is correct and that it is correctly
        written to file.
        """
        det = create_multiperiod_data()

        with h5py.File(FILENAME, 'w') as file:
            det.save_nxs2(file)
        del det

        with h5py.File(FILENAME, 'r') as file:
            load_det = read_detector1_from_histogram(file)

        self.assertEqual(load_det._dict['resolution'], 1)
        self.assertArrays(load_det._dict['raw_time'], [1, 2, 3])
        self.assertArrays(load_det._dict['spectrum_index'], [4, 5])
        self.assertEqual(load_det._dict['inst'], 'python')
        self.assertEqual(load_det._dict['time_zero'], 3)
        self.assertEqual(load_det._dict['first_good'], 4)
        self.assertEqual(load_det._dict['last_good'], 42)
        self.assertArrays(load_det._dict['counts'], [
                                                     [[1, 1, 1], [1, 1, 1]],
                                                     [[2, 2, 2], [2, 2, 2]],
                                                     [[3, 3, 3], [3, 3, 3]]])
        self.assertEqual(load_det.N_x, 3)
        self.assertEqual(load_det.N_hist, 2)
        self.assertEqual(load_det.N_periods, 3)

        os.remove(FILENAME)


if __name__ == '__main__':
    unittest.main()
