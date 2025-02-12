from MuonDataLib.data.utils import NONE
from MuonDataLib.data.sample_logs import SampleLogs

from MuonDataLib.test_helpers.unit_test import TestHelper
import numpy as np
import unittest
import h5py
import os


FILENAME = 'logs.nxs'


class SampleLogsTest(TestHelper):

    def setUp(self):
        self.logs = SampleLogs()

    def test_init_(self):
        self.assertEqual(self.logs._float_dict, {})
        self.assertEqual(self.logs._int_dict, {})
        self.assertEqual(self.logs._look_up, {})

    def test_add_sample_log_float(self):
        self.logs.add_sample_log('float test',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3.1, 4.1], dtype=np.double))

        self.assertEqual(list(self.logs._float_dict.keys()), ['float test'])
        tmp = self.logs._float_dict['float test']
        self.assertArrays(tmp.x, np.asarray([1.1, 2.1]))
        self.assertArrays(tmp.y, np.asarray([3.1, 4.1]))
        self.assertEqual(self.logs._int_dict, {})
        self.assertEqual(list(self.logs._look_up.keys()), ['float test'])
        self.assertEqual(self.logs._look_up['float test'], 'float')

    def test_get_sample_log_float(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3.1, 4.1], dtype=np.double))

        self.logs.add_sample_log('test',
                                 np.asarray([31.1, 32.1], dtype=np.double),
                                 np.asarray([34.1, 44.1], dtype=np.double))

        tmp = self.logs.get_sample_log('unit')
        self.assertArrays(tmp.x, np.asarray([1.1, 2.1]))
        self.assertArrays(tmp.y, np.asarray([3.1, 4.1]))

        tmp = self.logs.get_sample_log('test')
        self.assertArrays(tmp.x, np.asarray([31.1, 32.1]))
        self.assertArrays(tmp.y, np.asarray([34.1, 44.1]))

    def test_clear(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3, 4], dtype=np.double))

        self.logs.add_sample_log('test',
                                 np.asarray([31.1, 32.1], dtype=np.double),
                                 np.asarray([4.3, 4.4], dtype=np.double))

        tmp = self.logs.get_sample_log('unit')
        self.assertArrays(tmp.x, np.asarray([1.1, 2.1]))
        self.assertArrays(tmp.y, np.asarray([3, 4]))

        tmp = self.logs.get_sample_log('test')
        self.assertArrays(tmp.x, np.asarray([31.1, 32.1]))
        self.assertArrays(tmp.y, np.asarray([4.3, 4.4]))

        self.logs.clear()
        self.assertEqual(self.logs._float_dict, {})
        self.assertEqual(self.logs._int_dict, {})
        self.assertEqual(self.logs._look_up, {})

    def test_get_names(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3, 4], dtype=np.double))

        self.logs.add_sample_log('test',
                                 np.asarray([31.1, 32.1], dtype=np.double),
                                 np.asarray([4.3, 4.4], dtype=np.double))

        self.assertArrays(self.logs.get_names(), ['unit', 'test'])

    def test_add_and_get_filter_float(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3.1, 4.1], dtype=np.double))

        self.logs.add_sample_log('test',
                                 np.asarray([31.1, 32.1], dtype=np.double),
                                 np.asarray([4.3, 4.4], dtype=np.double))
        self.logs.add_filter('unit', -2.2, 8.9)

        tmp = self.logs.get_sample_log('unit')
        result = tmp.get_filter()
        self.assertEqual(result[0], 'unit_filter')
        self.assertArrays(result[1], np.asarray([1.1, 2.1]))
        self.assertArrays(result[2], np.asarray([3.1, 4.1]))
        self.assertEqual(result[3], -2.2)
        self.assertEqual(result[4], 8.9)

        tmp = self.logs.get_sample_log('test')
        result = tmp.get_filter()
        self.assertEqual(result[0], '')
        self.assertArrays(result[1], np.asarray([31.1, 32.1]))
        self.assertArrays(result[2], np.asarray([4.3, 4.4]))
        self.assertEqual(result[3], NONE)
        self.assertEqual(result[4], NONE)

    def test_apply_filter_float(self):
        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(-5, 5, 1, dtype=np.double))
        self.logs.add_filter('unit', -1, 1)
        times = np.asarray([np.asarray([-1., 1], dtype=np.double)])
        self.logs.apply_filter(times)
        tmp = self.logs.get_sample_log('unit')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([-5, -4, -3, -2, 2, 3, 4],
                                         dtype=np.double))

    def test_save_nxs2_no_filter(self):
        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(5, 10, 1, dtype=np.double))

        self.logs.add_sample_log('test',
                                 np.arange(15, 20, 1, dtype=np.double),
                                 np.arange(25, 30, 1, dtype=np.double))

        with h5py.File(FILENAME, 'w') as file:
            self.logs.save_nxs2(file)
        del self.logs

        with h5py.File(FILENAME, 'r') as file:
            tmp = file['raw_data_1']['selog']
            self.compare_keys(tmp, ['unit', 'test'])

            log = tmp['unit']['value_log']
            x = np.arange(-5, 5, 1, dtype=np.double)
            y = np.arange(5, 10, 1, dtype=np.double)

            self.assertArrays(log['time'], x)
            self.assertArrays(log['value'], y)
            log = tmp['test']['value_log']
            x = np.arange(15, 20, 1, dtype=np.double)
            y = np.arange(25, 30, 1, dtype=np.double)
            self.assertArrays(log['time'], x)
            self.assertArrays(log['value'], y)
        os.remove(FILENAME)

    def test_save_nxs2_with_filter(self):
        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(5, 10, 1, dtype=np.double))
        x = np.arange(0, 3, 1, dtype=np.double)
        y = np.arange(6, 9, 1, dtype=np.double)

        self.logs._float_dict['unit'].set_filter_values(x, y)

        self.logs.add_sample_log('test',
                                 np.arange(15, 20, 1, dtype=np.double),
                                 np.arange(25, 30, 1, dtype=np.double))
        x = np.arange(17, 19, 1, dtype=np.double)
        y = np.arange(27, 29, 1, dtype=np.double)

        self.logs._float_dict['test'].set_filter_values(x, y)

        with h5py.File(FILENAME, 'w') as file:
            self.logs.save_nxs2(file)
        del self.logs

        with h5py.File(FILENAME, 'r') as file:
            tmp = file['raw_data_1']['selog']
            self.compare_keys(tmp, ['unit', 'test'])

            log = tmp['unit']['value_log']
            self.assertArrays(log['time'],
                              np.arange(0, 3, 1, dtype=np.double))
            self.assertArrays(log['value'],
                              np.arange(6, 9, 1, dtype=np.double))
            log = tmp['test']['value_log']
            self.assertArrays(log['time'],
                              np.arange(17, 19, 1, dtype=np.double))
            self.assertArrays(log['value'],
                              np.arange(27, 29, 1, dtype=np.double))
        os.remove(FILENAME)

    def test_clear_filters(self):
        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(5, 10, 1, dtype=np.double))
        self.logs.add_filter('unit', -.1, .1)
        self.logs.add_sample_log('test',
                                 np.arange(15, 20, 1, dtype=np.double),
                                 np.arange(25, 30, 1, dtype=np.double))

        self.logs.add_filter('test', .5, .7)

        self.assertEqual(len(self.logs.get_names()), 2)

        tmp = self.logs.get_sample_log('unit')
        self.assertEqual(tmp._min, -.1)
        self.assertEqual(tmp._max, .1)

        tmp = self.logs.get_sample_log('test')
        self.assertEqual(tmp._min, .5)
        self.assertEqual(tmp._max, .7)

        self.logs.clear_filters()
        self.assertEqual(len(self.logs.get_names()), 2)

        tmp = self.logs.get_sample_log('unit')
        self.assertEqual(tmp._min, NONE)
        self.assertEqual(tmp._max, NONE)

        tmp = self.logs.get_sample_log('test')
        self.assertEqual(tmp._min, NONE)
        self.assertEqual(tmp._max, NONE)


if __name__ == '__main__':
    unittest.main()
