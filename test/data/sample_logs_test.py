from MuonDataLib.data.utils import NONE
from MuonDataLib.data.sample_logs import (LogData,
                                          SampleLogs)

from MuonDataLib.test_helpers.unit_test import TestHelper
import numpy as np
import unittest
import h5py
import os


FILENAME = 'logs.nxs'


class LogDataTest(TestHelper):

    def setUp(self):
        self.x = np.asarray([1, 2])
        self.y = np.asarray([3, 4])

        self.sample = LogData(self.x,
                              self.y)

    def test_init_(self):
        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertEqual(self.sample.fx, None)
        self.assertEqual(self.sample.fy, None)
        self.assertEqual(self.sample._name, None)
        self.assertEqual(self.sample._min, NONE)
        self.assertEqual(self.sample._max, NONE)

    def test_add_flters(self):
        self.sample.add_filter("test", 1.2, 3.4)

        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertEqual(self.sample.fx, None)
        self.assertEqual(self.sample.fy, None)
        self.assertEqual(self.sample._name, "test")
        self.assertEqual(self.sample._min, 1.2)
        self.assertEqual(self.sample._max, 3.4)

    def test_set_flter_values(self):
        fx = np.asarray([2, 1])
        fy = np.asarray([5, 6])

        self.sample.add_filter("test", 1.2, 3.4)
        self.sample.set_filter_values(fx, fy)
        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertArrays(self.sample.fx, fx)
        self.assertArrays(self.sample.fy, fy)
        self.assertEqual(self.sample._name, "test")
        self.assertEqual(self.sample._min, 1.2)
        self.assertEqual(self.sample._max, 3.4)

    def test_get_filter(self):
        self.sample.add_filter("test", 1.2, 3.4)
        result = self.sample.get_filter()
        self.assertEqual(result[0], 'test')
        self.assertArrays(result[1], self.x)
        self.assertArrays(result[2], self.y)
        self.assertEqual(result[3], 1.2)
        self.assertEqual(result[4], 3.4)

    def test_get_values_no_filter(self):
        x, y = self.sample.get_values()
        self.assertArrays(x, self.x)
        self.assertArrays(y, self.y)

    def test_get_values_filter(self):
        fx = np.asarray([2, 1])
        fy = np.asarray([5, 6])
        self.sample.set_filter_values(fx, fy)

        x, y = self.sample.get_values()
        self.assertArrays(x, fx)
        self.assertArrays(y, fy)

    def test_clear(self):
        fx = np.asarray([2, 1])
        fy = np.asarray([5, 6])
        self.sample.set_filter_values(fx, fy)
        self.sample.clear_filters()
        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertEqual(self.sample.fx, None)
        self.assertEqual(self.sample.fy, None)
        self.assertEqual(self.sample._name, None)
        self.assertEqual(self.sample._min, NONE)
        self.assertEqual(self.sample._max, NONE)


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

    def test_add_sample_log_int(self):
        self.logs.add_sample_log('int test',
                                 np.asarray([11.6, 12.6], dtype=np.double),
                                 np.asarray([31, 41], dtype=np.int32))

        self.assertEqual(list(self.logs._int_dict.keys()), ['int test'])
        tmp = self.logs._int_dict['int test']
        self.assertArrays(tmp.x, np.asarray([11.6, 12.6]))
        self.assertArrays(tmp.y, np.asarray([31, 41]))
        self.assertEqual(self.logs._float_dict, {})
        self.assertEqual(list(self.logs._look_up.keys()), ['int test'])
        self.assertEqual(self.logs._look_up['int test'], 'int')

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

    def test_get_sample_log_int(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3, 4], dtype=np.int32))

        self.logs.add_sample_log('test',
                                 np.asarray([31.1, 32.1], dtype=np.double),
                                 np.asarray([43, 44], dtype=np.int32))

        tmp = self.logs.get_sample_log('unit')
        self.assertArrays(tmp.x, np.asarray([1.1, 2.1]))
        self.assertArrays(tmp.y, np.asarray([3, 4]))

        tmp = self.logs.get_sample_log('test')
        self.assertArrays(tmp.x, np.asarray([31.1, 32.1]))
        self.assertArrays(tmp.y, np.asarray([43, 44]))

    def test_clear(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3, 4], dtype=np.int32))

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
                                 np.asarray([3, 4], dtype=np.int32))

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
        self.assertEqual(result[0], None)
        self.assertArrays(result[1], np.asarray([31.1, 32.1]))
        self.assertArrays(result[2], np.asarray([4.3, 4.4]))
        self.assertEqual(result[3], NONE)
        self.assertEqual(result[4], NONE)

    def test_add_and_get_filter_int(self):
        self.logs.add_sample_log('unit',
                                 np.asarray([1.1, 2.1], dtype=np.double),
                                 np.asarray([3, 4], dtype=np.int32))

        self.logs.add_sample_log('test',
                                 np.asarray([31.1, 32.1], dtype=np.double),
                                 np.asarray([43, 44], dtype=np.int32))
        self.logs.add_filter('unit', -2, 8)

        tmp = self.logs.get_sample_log('unit')
        result = tmp.get_filter()
        self.assertEqual(result[0], 'unit_filter')
        self.assertArrays(result[1], np.asarray([1.1, 2.1]))
        self.assertArrays(result[2], np.asarray([3, 4]))
        self.assertEqual(result[3], -2)
        self.assertEqual(result[4], 8)

        tmp = self.logs.get_sample_log('test')
        result = tmp.get_filter()
        self.assertEqual(result[0], None)
        self.assertArrays(result[1], np.asarray([31.1, 32.1]))
        self.assertArrays(result[2], np.asarray([43, 44]))
        self.assertEqual(result[3], NONE)
        self.assertEqual(result[4], NONE)

    def test_apply_filter_float(self):
        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(-5, 5, 1, dtype=np.double))
        self.logs.add_filter('unit', -1, 1)
        times = np.asarray([np.asarray([np.asarray([-1.], dtype=np.double),
                                       np.asarray([1.], dtype=np.double)])])
        self.logs.apply_filter('unit', times)
        tmp = self.logs.get_sample_log('unit')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([-5, -4, -3, -2, 2, 3, 4],
                                         dtype=np.double))

    def test_apply_filter_int(self):
        """
        *************not implemented yet***************************

        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(-5, 5, 1, dtype=np.int32))
        self.logs.add_filter('unit', -1, 1)
        times = np.asarray([-1., 0., 1.], dtype=np.double)
        self.logs.apply_filter('unit', times)
        tmp = self.logs.get_sample_log('unit')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([-5, -4, -3, -2, 2, 3, 4]))
        """
        pass

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
        x = np.arange(0, 3, 1, dtype=np.double),
        y = np.arange(6, 9, 1, dtype=np.double))

       self.logs._float_dict['unit'].set_filter_values(x, y)

        self.logs.add_sample_log('test',
                                 np.arange(15, 20, 1, dtype=np.double),
                                 np.arange(25, 30, 1, dtype=np.double))
        x = np.arange(17, 19, 1, dtype=np.double)
        y = np.arange(27, 29, 1, dtype=np.double))


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


if __name__ == '__main__':
    unittest.main()
