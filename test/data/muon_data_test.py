from MuonDataLib.data.utils import NONE
from MuonDataLib.data.muon_data import MuonData, MuonEventData
from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.test_helpers.unit_test import TestHelper
import unittest
import numpy as np
import os
import json
from unittest import mock


class fake_nxs_part(object):
    def __init__(self):
        self.save_nxs2 = mock.Mock(return_value='moo')

    def assert_called_once(self):
        self.save_nxs2.assert_called_once()


class MuonDataTest(unittest.TestCase):

    def test_MuonData_init(self):
        '''
        Instead of creating the full objects we
        will just use strings. Since we only need
        to check that the dict matches the
        argument correctly.
        For simplicity the strings used match
        the keys in the dict
        '''
        data = MuonData('sample',
                        'raw_data',
                        'source',
                        'user',
                        'periods',
                        'detector_1')

        for key in data._dict.keys():
            self.assertEqual(key, data._dict[key])

    def test_save_histogram(self):
        """
        Want to test that all of the individual
        parts are called when saving. So will use
        mocks.
        """
        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        data = MuonData(sample,
                        raw_data,
                        source,
                        user,
                        periods,
                        detector_1)
        data.save_histograms('tmp.nxs')

        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()

        os.remove('tmp.nxs')


class MuonEventDataTest(TestHelper, unittest.TestCase):

    @mock.patch('MuonDataLib.data.muon_data.SampleLogs')
    def test_MuonEventData_init(self, logs):
        '''
        Instead of creating the full objects we
        will just use strings. Since we only need
        to check that the dict matches the
        argument correctly.
        For simplicity the strings used match
        the keys in the dict
        '''
        data = MuonEventData('events',
                             'cache',
                             'sample',
                             'raw_data',
                             'source',
                             'user',
                             'periods',
                             'detector_1')
        logs.assert_called_once()

        for key in data._dict.keys():
            if key != 'logs':
                self.assertEqual(key, data._dict[key])
        self.assertEqual(data._events, 'events')
        self.assertEqual(data._cache, 'cache')

    def test_add_sample_log(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp', np.asarray([1, 2], dtype=np.double),
                            np.asarray([3, 4], dtype=np.double))
        data.add_sample_log('B', np.asarray([11, 12], dtype=np.double),
                            np.asarray([13, 14], dtype=np.double))

        self.assertEqual(data._cache.empty(), True)
        # check only 2 sample logs
        self.assertEqual(len(data._dict['logs']._look_up.keys()), 2)
        result = data._get_sample_log("Temp").get_values()
        self.assertArrays(result[0], np.asarray([1, 2]))
        self.assertArrays(result[1], np.asarray([3, 4]))

        result = data._get_sample_log("B").get_values()
        self.assertArrays(result[0], np.asarray([11, 12]))
        self.assertArrays(result[1], np.asarray([13, 14]))

    def test_add_sample_log_and_clear(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp', np.asarray([1, 2], dtype=np.double),
                            np.asarray([3, 4], dtype=np.double))
        data.histogram()
        self.assertEqual(data._cache.empty(), False)

        data.add_sample_log('B', np.asarray([11, 12], dtype=np.double),
                            np.asarray([13, 14], dtype=np.double))
        self.assertEqual(data._cache.empty(), True)
        # check only 2 sample logs
        self.assertEqual(len(data._dict['logs']._look_up.keys()), 2)
        result = data._get_sample_log("Temp").get_values()
        self.assertArrays(result[0], np.asarray([1, 2]))
        self.assertArrays(result[1], np.asarray([3, 4]))

        result = data._get_sample_log("B").get_values()
        self.assertArrays(result[0], np.asarray([11, 12]))
        self.assertArrays(result[1], np.asarray([13, 14]))

    def fill_cache(self, data):
        data._cache.save(np.asarray([np.asarray(
            [np.asarray([1, 2, 3], dtype=np.int32)])]),
                         np.asarray([0, 1, 2, 3], dtype=np.double),
                         np.asarray([1], dtype=np.int32),
                         np.asarray([0], dtype=np.int32),
                         0.1,
                         5.1,
                         0.0016,
                         6)
        self.assertEqual(data._cache.empty(), False)

    def test_keep_data_sample_log_below(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp',
                            np.asarray([1.0, 2.0], dtype=np.double),
                            np.asarray([3.0, 4.0], dtype=np.double))
        self.fill_cache(data)
        data.keep_data_sample_log_below("Temp", 3.3)
        self.assertEqual(data._cache.empty(), True)
        log = data._dict['logs']._float_dict['Temp']
        self.assertEqual(log._min, NONE)
        self.assertEqual(log._max, 3.3)

    def test_keep_data_sample_log_above(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp',
                            np.asarray([1.0, 2.0], dtype=np.double),
                            np.asarray([3.0, 4.0], dtype=np.double))
        self.fill_cache(data)
        data.keep_data_sample_log_above("Temp", 1.1)
        self.assertEqual(data._cache.empty(), True)
        log = data._dict['logs']._float_dict['Temp']
        self.assertEqual(log._min, 1.1)
        self.assertEqual(log._max, NONE)

    def test_keep_data_sample_log_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp',
                            np.asarray([1.0, 2.0], dtype=np.double),
                            np.asarray([3.0, 4.0], dtype=np.double))
        self.fill_cache(data)
        data.keep_data_sample_log_between("Temp", 1.1, 3.3)
        self.assertEqual(data._cache.empty(), True)
        log = data._dict['logs']._float_dict['Temp']
        self.assertEqual(log._min, 1.1)
        self.assertEqual(log._max, 3.3)

    def test_keep_data_sample_log_between_bad_values(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp',
                            np.asarray([1.0, 2.0], dtype=np.double),
                            np.asarray([3.0, 4.0], dtype=np.double))
        with self.assertRaises(RuntimeError):
            data.keep_data_sample_log_between("Temp", 7.1, 3.3)

    def test_only_keep_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        self.fill_cache(data)

        data.only_keep_data_time_between('first', 1, 2)
        self.assertEqual(data._cache.empty(), True)

        data.only_keep_data_time_between('second', 5, 7)

        self.assertArrays(list(data._keep_times.keys()), ['first', 'second'])
        self.assertArrays(data._keep_times['first'], np.asarray([1, 2]))
        self.assertArrays(data._keep_times['second'], np.asarray([5, 7]))

    def test_only_keep_data_time_between_duplicate(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.only_keep_data_time_between('first', 1, 2)
        with self.assertRaises(RuntimeError):
            data.only_keep_data_time_between('first', 3, 4)

    def test_only_keep_data_time_between_bad_times(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        self.fill_cache(data)
        with self.assertRaises(RuntimeError):
            data.only_keep_data_time_between('first', 6, 4)

    def test_remove_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        self.fill_cache(data)
        data.remove_data_time_between('one', 1, 2)
        self.assertEqual(data._cache.empty(), True)
        data.remove_data_time_between('two', 5, 7)

        self.assertEqual(len(data._time_filter), 2)

        start, end = data._time_filter['one']
        self.assertEqual(start, 1)
        self.assertEqual(end, 2)

        start, end = data._time_filter['two']
        self.assertEqual(start, 5)
        self.assertEqual(end, 7)

    def test_remove_data_time_between_duplicate(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        self.fill_cache(data)
        data.remove_data_time_between('one', 1, 2)
        with self.assertRaises(RuntimeError):
            data.remove_data_time_between('one', 5, 7)

    def test_remove_data_time_between_bad_values(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        self.fill_cache(data)
        with self.assertRaises(RuntimeError):
            data.remove_data_time_between('one', 4, 1)

    def test_delete_sample_log_filter(self):
        """
        This works for between, below and above
        """
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.add_sample_log('Temp',
                            np.asarray([1.0, 2.0], dtype=np.double),
                            np.asarray([3.0, 4.0], dtype=np.double))
        data.keep_data_sample_log_between("Temp", 1.1, 3.3)
        self.fill_cache(data)
        data.delete_sample_log_filter("Temp")
        self.assertEqual(data._cache.empty(), True)
        log = data._dict['logs']._float_dict['Temp']
        self.assertEqual(log._min, NONE)
        self.assertEqual(log._max, NONE)

    def test_delete_only_keep_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.only_keep_data_time_between('one', 1, 2)
        data.only_keep_data_time_between('two', 13, 24)
        self.fill_cache(data)
        data.delete_only_keep_data_time_between('one')
        self.assertEqual(data._cache.empty(), True)
        self.assertArrays(list(data._keep_times.keys()), ['two'])
        self.assertArrays(data._keep_times['two'], np.asarray([13, 24]))

    def test_delete_remove_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.remove_data_time_between('one', 1, 2)
        data.remove_data_time_between('two', 5, 7)
        self.fill_cache(data)

        self.assertEqual(len(data._time_filter), 2)

        data.delete_remove_data_time_between("two")
        self.assertEqual(data._cache.empty(), True)
        self.assertEqual(len(data._time_filter), 1)
        start, end = data._time_filter['one']
        self.assertEqual(start, 1)
        self.assertEqual(end, 2)

    def test_filter_remove_times(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.remove_data_time_between('one', 1, 2)
        data.remove_data_time_between('two', 5, 7)

        data._filter_remove_times()

        results = data._events.report_filters()
        self.assertEqual(len(results), 2)
        self.assertAlmostEqual(results['one'][0], 1e9, 3)
        self.assertAlmostEqual(results['one'][1], 2e9, 3)

        self.assertAlmostEqual(results['two'][0], 5e9, 3)
        self.assertAlmostEqual(results['two'][1], 7e9, 3)

    def test_filter_keep_times(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        data.only_keep_data_time_between('one', .01, .02)
        data.only_keep_data_time_between('two', .05, .06)

        data._filter_keep_times()

        results = data._events.report_filters()
        self.assertEqual(len(results), 3)
        self.assertAlmostEqual(results['keep_0'][0], 0, 3)
        self.assertAlmostEqual(results['keep_0'][1], 1e7, 3)

        self.assertAlmostEqual(results['keep_1'][0], 2e7, 3)
        self.assertAlmostEqual(results['keep_1'][1], 5e7, 3)

        self.assertAlmostEqual(results['keep_2'][0], 6e7, 3)
        self.assertAlmostEqual(results['keep_2'][1]/1.e9, 1.161, 3)

    def test_filter_logs(self):
        """
        This works for between, below and above
        """
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        x = np.arange(0.0, 1.0, 0.001, dtype=np.double)
        data.add_sample_log('Temp', x,
                            2*x)
        data.keep_data_sample_log_between("Temp", 0.0044, .163)
        data._filter_logs()

        results = data._events.report_filters()
        self.assertEqual(len(results), 2)
        self.assertAlmostEqual(results['Temp_filter_0'][0]/1e9, 0.0, 3)
        self.assertAlmostEqual(results['Temp_filter_0'][1]/1e9, 0.003, 3)

        self.assertAlmostEqual(results['Temp_filter_1'][0]/1e9, 0.081, 3)
        self.assertAlmostEqual(results['Temp_filter_1'][1]/1e9, 0.999, 3)

    def test_filters(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        x = np.arange(0.0, 1.0, 0.001, dtype=np.double)
        data.add_sample_log('Temp', x,
                            2*x)
        data.keep_data_sample_log_between("Temp", 0.0044, .163)
        data.only_keep_data_time_between('first', .01, .02)
        data.only_keep_data_time_between('second', .05, .06)

        data.remove_data_time_between('one', 1, 2)
        data.remove_data_time_between('two', 5, 7)

        data._filters()

        results = data._events.report_filters()
        self.assertEqual(len(results), 7)
        self.assertAlmostEqual(results['Temp_filter_0'][0]/1e9, 0.0, 3)
        self.assertAlmostEqual(results['Temp_filter_0'][1]/1e9, 0.003, 3)

        self.assertAlmostEqual(results['Temp_filter_1'][0]/1e9, 0.081, 3)
        self.assertAlmostEqual(results['Temp_filter_1'][1]/1e9, 0.999, 3)

        self.assertAlmostEqual(results['keep_0'][0], 0, 3)
        self.assertAlmostEqual(results['keep_0'][1], 1e7, 3)

        self.assertAlmostEqual(results['keep_1'][0], 2e7, 3)
        self.assertAlmostEqual(results['keep_1'][1], 5e7, 3)

        self.assertAlmostEqual(results['keep_2'][0], 6e7, 3)
        self.assertAlmostEqual(results['keep_2'][1]/1.e9, 1.161, 3)

        self.assertAlmostEqual(results['one'][0], 1e9, 3)
        self.assertAlmostEqual(results['one'][1], 2e9, 3)

        self.assertAlmostEqual(results['two'][0], 5e9, 3)
        self.assertAlmostEqual(results['two'][1], 7e9, 3)

    def test_clear_filters(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        x = np.arange(0.0, 1.0, 0.001, dtype=np.double)
        data.add_sample_log('Temp', x,
                            2*x)
        data.keep_data_sample_log_between("Temp", 0.0044, .163)
        data.only_keep_data_time_between('first', .01, .02)
        data.only_keep_data_time_between('second', .05, .06)

        data.remove_data_time_between('one', 1, 2)
        data.remove_data_time_between('two', 5, 7)
        self.fill_cache(data)
        data.clear_filters()

        self.assertEqual(data._cache.empty(), True)

        log = data._dict['logs']._float_dict['Temp']
        self.assertEqual(log._min, NONE)
        self.assertEqual(log._max, NONE)

        self.assertEqual(data._keep_times, {})
        self.assertEqual(data._time_filter, {})

    def test_save_histogram_empty_cache(self):
        """
        Want to test that all of the individual
        parts are called when saving. So will use
        mocks.
        """

        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        events = mock.Mock()
        events.histogram = mock.Mock(return_value=([1], [2]))
        events.report_filters = mock.Mock(return_value={'a': [1, 3]})

        cache = mock.Mock()
        cache.empty = mock.Mock(return_value=True)

        data = MuonEventData(events,
                             cache,
                             sample,
                             raw_data,
                             source,
                             user,
                             periods,
                             detector_1)
        data.save_histograms('tmp.nxs')

        cache.empty.assert_called_once()
        events.histogram.assert_called_once_with(width=0.016, cache=cache)
        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()

        os.remove('tmp.nxs')

    def test_histogram_with_logs_no_cache(self):
        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        events = mock.Mock()
        events.histogram = mock.Mock(return_value=([1], [2]))
        events.report_filters = mock.Mock(return_value={'a': [1, 3]})
        events.apply_log_filter = mock.Mock()

        cache = mock.Mock()
        cache.empty = mock.Mock(return_value=True)
        cache.get_resolution = mock.MagicMock(return_value=0.016)
        cache.get_histograms = mock.MagicMock(return_value=([1], [2]))
        data = MuonEventData(events,
                             cache,
                             sample,
                             raw_data,
                             source,
                             user,
                             periods,
                             detector_1)
        data.add_sample_log('B',
                            np.asarray([1], dtype=np.double),
                            np.asarray([2], dtype=np.double))
        data.add_sample_log('T',
                            np.asarray([3], dtype=np.double),
                            np.asarray([4], dtype=np.double))
        data._dict['logs'].apply_filter = mock.Mock()
        data.histogram(0.016)

        cache.empty.assert_called_once()
        events.histogram.assert_called_once_with(width=0.016, cache=cache)
        self.assertEqual(1, data._dict['logs'].apply_filter.call_count)
        self.assertEqual(2, events.apply_log_filter.call_count)

    def test_histogram_with_logs_with_cache(self):
        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        events = mock.Mock()
        events.histogram = mock.Mock(return_value=([1], [2]))
        events.report_filters = mock.Mock(return_value={'a': [1, 3]})
        events.apply_log_filter = mock.Mock()

        cache = mock.Mock()
        cache.empty = mock.Mock(return_value=False)
        cache.get_resolution = mock.MagicMock(return_value=0.016)
        cache.get_histograms = mock.MagicMock(return_value=([1], [2]))
        data = MuonEventData(events,
                             cache,
                             sample,
                             raw_data,
                             source,
                             user,
                             periods,
                             detector_1)
        data.add_sample_log('B',
                            np.asarray([1], dtype=np.double),
                            np.asarray([2], dtype=np.double))
        data.add_sample_log('T',
                            np.asarray([3], dtype=np.double),
                            np.asarray([4], dtype=np.double))
        data._dict['logs'].apply_filter = mock.Mock()
        data.histogram(0.016)

        cache.empty.assert_called_once()
        self.assertEqual(0, events.histogram.call_count)
        self.assertEqual(0, events.apply_log_filter.call_count)
        self.assertEqual(0, data._dict['logs'].apply_filter.call_count)

    def test_histogram_with_logs_with_cache_new_resolution(self):
        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        events = mock.Mock()
        events.histogram = mock.Mock(return_value=([1], [2]))
        events.report_filters = mock.Mock(return_value={'a': [1, 3]})
        events.apply_log_filter = mock.Mock()

        cache = mock.Mock()
        cache.empty = mock.Mock(return_value=False)
        cache.get_resolution = mock.MagicMock(return_value=0.016)
        cache.get_histograms = mock.MagicMock(return_value=([1], [2]))
        data = MuonEventData(events,
                             cache,
                             sample,
                             raw_data,
                             source,
                             user,
                             periods,
                             detector_1)
        data.add_sample_log('B',
                            np.asarray([1], dtype=np.double),
                            np.asarray([2], dtype=np.double))
        data.add_sample_log('T',
                            np.asarray([3], dtype=np.double),
                            np.asarray([4], dtype=np.double))
        data._dict['logs'].apply_filter = mock.Mock()
        data.histogram(0.01)

        cache.empty.assert_called_once()
        self.assertEqual(1, events.histogram.call_count)
        self.assertEqual(0, events.apply_log_filter.call_count)
        self.assertEqual(0, data._dict['logs'].apply_filter.call_count)

    def test_save_histogram_occupied_cache(self):
        """
        Want to test that all of the individual
        parts are called when saving. So will use
        mocks.
        """
        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        events = mock.Mock()
        events.histogram = mock.Mock(return_value=([1], [2]))
        events.report_filters = mock.Mock(return_value={'a': [1, 3]})

        cache = mock.Mock()
        cache.empty = mock.Mock(return_value=False)
        cache.get_resolution = mock.MagicMock(return_value=0.016)
        cache.get_histograms = mock.MagicMock(return_value=([1], [2]))
        data = MuonEventData(events,
                             cache,
                             sample,
                             raw_data,
                             source,
                             user,
                             periods,
                             detector_1)
        data.save_histograms('tmp.nxs')

        cache.empty.assert_called_once()
        events.histogram.assert_not_called()
        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()

        os.remove('tmp.nxs')

    def test_save_histogram(self):
        """
        Want to test that all of the individual
        parts are called when saving. So will use
        mocks.
        """
        events = mock.MagicMock()
        events.report_filters = mock.Mock(return_value={})
        events.histogram = mock.Mock(return_value=([1, 1], [2]))
        cache = mock.MagicMock()
        cache.empty = mock.MagicMock(return_value=True)
        sample = fake_nxs_part()
        raw_data = fake_nxs_part()
        source = fake_nxs_part()
        user = fake_nxs_part()
        periods = fake_nxs_part()
        detector_1 = fake_nxs_part()

        data = MuonEventData(events,
                             cache,
                             sample,
                             raw_data,
                             source,
                             user,
                             periods,
                             detector_1)
        data.add_sample_log('T',
                            np.arange(0, 5, dtype=np.double),
                            np.arange(5, 10, dtype=np.double))
        data._dict['logs'].save_nxs2 = mock.Mock()
        data.save_histograms('tmp.nxs')

        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()
        data._dict['logs'].save_nxs2.assert_called_once()
        os.remove('tmp.nxs')

    def test_get_frame_start_times(self):
        """
        Test this with some "real" data.
        I could mock the data, but if I transition
        to C++ later with a Python interface then
        the object might be constructed in the C++.
        So we will not be able to mock it.
        """
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        start_time = data.get_frame_start_times()

        self.assertArrays(start_time, np.asarray([0.0,
                                                  0.02012,
                                                  0.04023,
                                                  0.06035,
                                                  0.08046,
                                                  0.1006,
                                                  0.1207,
                                                  0.1408,
                                                  0.1609]))

    def test_report_raw_filters(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)

        data.remove_data_time_between('one', 1, 2)
        data._filters()
        results = data._report_raw_filters()

        self.assertEqual(len(results), 1)

        self.assertAlmostEqual(results['one'][0], 1, 3)
        self.assertAlmostEqual(results['one'][1], 2, 3)

    def add_filters_for_report(self, data):
        x = np.arange(0.0, 1.0, 0.001, dtype=np.double)
        data.add_sample_log('Temp', x,
                            2*x)
        data.keep_data_sample_log_between("Temp", 0.0044, .163)
        data.only_keep_data_time_between('first', .01, .02)
        data.only_keep_data_time_between('second', .05, .06)

        data.remove_data_time_between('one', 1, 2)
        data.remove_data_time_between('two', 5, 7)

    def expected_report(self, result):
        self.assertArrays(list(result.keys()),
                          ['sample_log_filters',
                           'time_filters'])

        self.assertArrays(list(result['time_filters'].keys()),
                          ['keep_filters',
                           'remove_filters'])
        tmp = result['time_filters']['remove_filters']
        self.assertArrays(list(tmp.keys()), ['one', 'two'])
        self.assertArrays(tmp['one'], [1, 2])
        self.assertArrays(tmp['two'], [5, 7])

        tmp = result['time_filters']['keep_filters']
        self.assertArrays(list(tmp.keys()), ['first', 'second'])
        self.assertArrays(tmp['first'], [0.01, 0.02])
        self.assertArrays(tmp['second'], [0.05, 0.06])

        tmp = result['sample_log_filters']
        self.assertArrays(list(tmp.keys()), ['Temp'])
        self.assertArrays(tmp['Temp'], [0.0044, 0.163])

    def test_report_filters(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)

        self.add_filters_for_report(data)

        result = data.report_filters()

        self.expected_report(result)

    def test_save_filters(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)

        self.add_filters_for_report(data)

        data.save_filters('muon_test.json')

        with open('muon_test.json') as file:
            result = json.load(file)

        self.expected_report(result)
        os.remove('muon_test.json')

    def test_load_filters(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        data = load_events(file, 64)
        x = np.arange(0.0, 1.0, 0.001, dtype=np.double)
        data.add_sample_log('Temp', x,
                            2*x)

        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'load_filter.json')
        data.load_filters(file)
        result = data.report_filters()
        self.expected_report(result)

    """
    These tests are to check that the event filters
    are cleared correctly - indirectly test the _clear
    method.
    """
    def test_clear_add_sample_log(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        data.remove_data_time_between('first', 1, 1.2)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # add a sample log
        x = np.arange(0.0, 1.0, 0.001, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_keep_data_sample_log_below(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        data.remove_data_time_between('first', 1, 1.2)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # add filter
        data.keep_data_sample_log_below('Temp2', 2.3)
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_keep_data_sample_log_above(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        data.remove_data_time_between('first', 1, 1.2)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # add filter
        data.keep_data_sample_log_above('Temp2', 1.3)
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_keep_data_sample_log_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        data.remove_data_time_between('first', 1, 1.2)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # add filter
        data.keep_data_sample_log_between('Temp2', 1.3, 2.6)
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_keep_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        data.keep_data_sample_log_between('Temp2', 1.3, 2.6)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # add filter
        data.only_keep_data_time_between('one', 1.3, 2.6)
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_remove_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        data.keep_data_sample_log_between('Temp2', 1.3, 2.6)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # add filter
        data.remove_data_time_between('one', 1.3, 2.6)
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_delete_sample_log_filter(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        data.keep_data_sample_log_between('Temp2', 1.3, 2.6)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # remove filter
        data.delete_sample_log_filter('Temp2')
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_delete_only_keep_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        # this adds 2 event filters one either side
        data.only_keep_data_time_between('first', 1, 1.2)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 2)

        # remove filter
        data.delete_only_keep_data_time_between('first')
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)

    def test_clear_delete_remove_data_time_between(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        x = np.arange(1, 3.0, 0.1, dtype=np.double)
        data.add_sample_log('Temp2', x,
                            2*x)
        # this adds 2 event filters one either side
        data.remove_data_time_between('first', 1, 1.2)
        # update event filters
        data.histogram()
        self.assertEqual(len(data._events.report_filters()), 1)

        # remove filter
        data.delete_remove_data_time_between('first')
        # check the event filters are now empty
        self.assertEqual(len(data._events.report_filters()), 0)


if __name__ == '__main__':
    unittest.main()
