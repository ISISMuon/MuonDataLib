from MuonDataLib.data.utils import NONE
from MuonDataLib.cython_ext.base_sample_logs import (LogData,
                                                     BaseSampleLogs)

from MuonDataLib.test_helpers.unit_test import TestHelper
import numpy as np
import unittest


class LogDataTest(TestHelper):

    def setUp(self):
        self.x = np.asarray([1, 2], dtype=np.double)
        self.y = np.asarray([3, 4], dtype=np.double)

        self.sample = LogData(self.x,
                              self.y)

    def test_init_(self):
        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertArrays(np.asarray(self.sample.fx),
                          np.asarray([], dtype=np.double))
        self.assertArrays(np.asarray(self.sample.fy),
                          np.asarray([], dtype=np.double))
        self.assertEqual(self.sample._name, '')
        self.assertEqual(self.sample._min, NONE)
        self.assertEqual(self.sample._max, NONE)

    def test_add_flters(self):
        self.sample.add_filter("test", 1.2, 3.4)

        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertArrays(np.asarray(self.sample.fx),
                          np.asarray([], dtype=np.double))
        self.assertArrays(np.asarray(self.sample.fy),
                          np.asarray([], dtype=np.double))
        self.assertEqual(self.sample._name, "test")
        self.assertEqual(self.sample._min, 1.2)
        self.assertEqual(self.sample._max, 3.4)

    def test_set_flter_values(self):
        fx = np.asarray([2, 1], dtype=np.double)
        fy = np.asarray([5, 6], dtype=np.double)

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
        fx = np.asarray([2, 1], dtype=np.double)
        fy = np.asarray([5, 6], dtype=np.double)
        self.sample.set_filter_values(fx, fy)

        x, y = self.sample.get_values()
        self.assertArrays(x, fx)
        self.assertArrays(y, fy)

    def test_get_original_values(self):
        fx = np.asarray([2, 1], dtype=np.double)
        fy = np.asarray([5, 6], dtype=np.double)
        self.sample.set_filter_values(fx, fy)

        x, y = self.sample.get_original_values()
        self.assertArrays(x, self.x)
        self.assertArrays(y, self.y)

    def test_clear(self):
        fx = np.asarray([2, 1], dtype=np.double)
        fy = np.asarray([5, 6], dtype=np.double)
        self.sample.set_filter_values(fx, fy)
        self.sample.clear_filters()
        self.assertArrays(self.sample.x, self.x)
        self.assertArrays(self.sample.y, self.y)
        self.assertArrays(np.asarray(self.sample.fx),
                          np.asarray([], dtype=np.double))
        self.assertArrays(np.asarray(self.sample.fy),
                          np.asarray([], dtype=np.double))
        self.assertEqual(self.sample._name, '')
        self.assertEqual(self.sample._min, NONE)
        self.assertEqual(self.sample._max, NONE)


class BaseSampleLogsTest(TestHelper):

    def setUp(self):
        self.logs = BaseSampleLogs()

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
        self.logs.add_sample_log('test',
                                 np.arange(0, 10, 1, dtype=np.double),
                                 np.arange(20, 15, -0.5, dtype=np.double))
        self.logs.add_filter('unit', -1, 1)
        times = np.asarray([np.asarray([-1., 1], dtype=np.double)])
        self.logs.apply_filter(times)

        tmp = self.logs.get_sample_log('unit')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([-5, -4, -3, -2, 2, 3, 4],
                                         dtype=np.double))

        tmp = self.logs.get_sample_log('test')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([2, 3, 4, 5, 6, 7, 8, 9],
                                         dtype=np.double))

    def test_apply_filter_float_rm_below(self):
        self.logs.add_sample_log('unit',
                                 np.arange(-5, 5, 1, dtype=np.double),
                                 np.arange(-5, 5, 1, dtype=np.double))
        self.logs.add_sample_log('test',
                                 np.arange(0, 10, 1, dtype=np.double),
                                 np.arange(20, 15, -0.5, dtype=np.double))
        self.logs.add_filter('unit', -1, NONE)
        times = np.asarray([np.asarray([-5., -1], dtype=np.double)])
        self.logs.apply_filter(times)

        tmp = self.logs.get_sample_log('unit')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([0, 1, 2, 3, 4],
                                         dtype=np.double))

        tmp = self.logs.get_sample_log('test')
        fx, fy = tmp.get_values()
        self.assertArrays(fx, np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9],
                                         dtype=np.double))

    def test_apply_filter_change_float(self):
        """
        This tests a bug that meant the new filter
        was applied to the old filtered data.
        """
        self.logs.add_sample_log('unit',
                                 np.arange(0, 10, 1, dtype=np.double),
                                 np.arange(-5, 5, 1, dtype=np.double))
        self.logs.add_sample_log('test',
                                 np.arange(0, 10, 1, dtype=np.double),
                                 np.arange(20, 15, -0.5, dtype=np.double))
        # add original filter
        self.logs.add_filter('unit', -1, NONE)
        times = np.asarray([np.asarray([0., 4], dtype=np.double)])
        self.logs.apply_filter(times)

        # check that the first filter is applied
        fx, fy = self.logs.get_sample_log('unit').get_values()
        self.assertArrays(fx, np.asarray([5, 6, 7, 8, 9],
                                         dtype=np.double))

        self.assertArrays(fy, np.asarray([0, 1, 2, 3, 4],
                                         dtype=np.double))

        fx, fy = self.logs.get_sample_log('test').get_values()
        self.assertArrays(fx, np.asarray([5, 6, 7, 8, 9],
                                         dtype=np.double))
        self.assertArrays(fy, np.asarray([17.5, 17, 16.5, 16, 15.5],
                                         dtype=np.double))

        # clear filter and apply a new one
        self.logs.clear_filter('unit')

        # apply new filter
        self.logs.add_filter('unit', NONE, 5)
        times = np.asarray([np.asarray([5, 10], dtype=np.double)])
        self.logs.apply_filter(times)

        # check just the new filter is applied
        fx, fy = self.logs.get_sample_log('unit').get_values()
        self.assertArrays(fx, np.asarray([0, 1, 2, 3, 4],
                                         dtype=np.double))
        self.assertArrays(fy, np.asarray([-5, -4, -3, -2, -1],
                                         dtype=np.double))

        # previously this would have a result of no data
        fx, fy = self.logs.get_sample_log('test').get_values()
        self.assertArrays(fx, np.asarray([0, 1, 2, 3, 4],
                                         dtype=np.double))
        self.assertArrays(fy, np.asarray([20, 19.5, 19,
                                          18.5, 18], dtype=np.double))

    def test_clear_filter(self):
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

        self.logs.clear_filter('test')
        self.assertEqual(len(self.logs.get_names()), 2)

        tmp = self.logs.get_sample_log('unit')
        self.assertEqual(tmp._min, -.1)
        self.assertEqual(tmp._max, .1)

        tmp = self.logs.get_sample_log('test')
        self.assertEqual(tmp._min, NONE)
        self.assertEqual(tmp._max, NONE)

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
