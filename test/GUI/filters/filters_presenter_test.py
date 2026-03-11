import unittest
from unittest import mock
from MuonDataLib.GUI.filters.presenter import FilterPresenter
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.data.loader.load_events import load_events
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from data_paths import FILE  # noqa: E402


TT = '_time-table'


class FilterPresenterTest(TestHelper):

    def setUp(self):
        self.presenter = FilterPresenter()

    def test_show_file_match(self):
        name = 'test.json'
        """
        lets use fake values (should be dicts,
        but just checks they match)
        """
        self.presenter._time_file_data = 'time'
        self.presenter._log_file_data = 'log'

        self.assertFalse(self.presenter.show_file(name, 'time', 'log'))

    def test_show_file_time_match(self):
        name = 'test.json'
        """
        lets use fake values (should be dicts,
        but just checks they match)
        """
        self.presenter._time_file_data = 'time'
        self.presenter._log_file_data = 'log'

        self.assertTrue(self.presenter.show_file(name, 'time', 'new'))

    def test_show_file_log_match(self):
        name = 'test.json'
        """
        lets use fake values (should be dicts,
        but it just checks the values match)
        """
        self.presenter._time_file_data = 'time'
        self.presenter._log_file_data = 'log'

        self.assertTrue(self.presenter.show_file(name, 'new', 'log'))

    def test_show_file_no_match(self):
        name = 'test.json'
        """
        lets use fake values (should be dicts,
        but just checks they match)
        """
        self.presenter._time_file_data = 'time'
        self.presenter._log_file_data = 'log'

        self.assertTrue(self.presenter.show_file(name, 'unit', 'test'))

    def test_headers(self):
        self.assertEqual(len(self.presenter.headers), 3)

    def test_set_data(self):
        class MockData(object):
            def __init__(self):
                self._dict = {'logs': 'log data'}

            def get_frame_start_times(self):
                return [1, 2, 6]

        data = MockData()

        self.presenter._time.set_time_range = mock.Mock()

        self.presenter.set_data(data)
        self.presenter._time.set_time_range.assert_called_with(1, 6 + 32e-6)
        self.assertEqual(self.presenter._log._logs, 'log data')

    def cf_filters(self, result, expect):
        self.assertEqual(len(result), 3)

        self.assertEqual(result['peak_property']['Amplitudes'],
                         expect[0])
        self.assertEqual(result['sample_log_filters'],
                         expect[1])
        self.assertEqual(result['time_filters']['keep_filters'],
                         expect[2])
        self.assertEqual(result['time_filters']['remove_filters'],
                         expect[3])

    def test_apply_filters_none(self):
        filters = []
        self.presenter._data = load_events(FILE, 64)
        self.presenter.apply_filters(filters,
                                     'Include',
                                     [])
        result = self.presenter._data.report_filters()

        expect = [0, {}, {}, {}]
        self.cf_filters(result, expect)

    def test_apply_filters_include(self):
        filters = [{'Name' + TT: 'unit',
                    'Start' + TT: 0.1,
                    'End' + TT: 0.5},
                   {'Name' + TT: 'test',
                    'Start' + TT: 0.7,
                    'End' + TT: 1.2}]

        self.presenter._data = load_events(FILE, 64)
        self.presenter.apply_filters(filters,
                                     'Include',
                                     [])
        result = self.presenter._data.report_filters()

        expect = [0,
                  {},
                  {'unit': [0.1, 0.5],
                   'test': [0.7, 1.2]},
                  {}]
        self.cf_filters(result, expect)

    def test_apply_filters_exclude(self):
        filters = [{'Name' + TT: 'unit',
                    'Start' + TT: 0.1,
                    'End' + TT: 0.5},
                   {'Name' + TT: 'test',
                    'Start' + TT: 0.7,
                    'End' + TT: 1.2}]

        self.presenter._data = load_events(FILE, 64)
        self.presenter.apply_filters(filters,
                                     'Exclude',
                                     [])
        result = self.presenter._data.report_filters()
        expect = [0,
                  {},
                  {},
                  {'unit': (0.1, 0.5),
                   'test': (0.7, 1.2)},
                  ]
        self.cf_filters(result, expect)

    def test_calculate_no_filters(self):
        self.presenter._data = load_events(FILE, 64)
        N_str, err_msg = self.presenter.calculate(1, {}, 'Exclude', [])
        self.assertEqual(err_msg, '')
        self.assertEqual(N_str.children,
                         'Number of events: 64,147')

    def test_calculate_with_exclude_filter(self):
        self.presenter._data = load_events(FILE, 64)
        filters = [{'Name' + TT: 'unit', 'Start' + TT: 0.1, 'End' + TT: 1.2}]
        N_str, err_msg = self.presenter.calculate(1, filters, 'Exclude', [])
        self.assertEqual(err_msg, '')
        self.assertEqual(N_str.children,
                         'Number of events: 57,653')

    def test_calculate_with_include_filter(self):
        self.presenter._data = load_events(FILE, 64)
        filters = [{'Name' + TT: 'unit', 'Start' + TT: 0.1, 'End' + TT: 1.2}]
        N_str, err_msg = self.presenter.calculate(1, filters, 'Include', [])
        self.assertEqual(err_msg, '')
        self.assertEqual(N_str.children,
                         'Number of events: 5,037')

    def test_calculate_with_error(self):
        def throw(filters, state, log):
            raise RuntimeError("mock throw")

        self.presenter._data = load_events(FILE, 64)
        self.presenter.apply_filters = mock.Mock(side_effect=throw)
        filters = [{'Name_t': 'unit', 'Start_t': 0.1, 'End_t': 1.2}]
        N_str, err_msg = self.presenter.calculate(1, filters, 'Include', [])
        self.assertEqual(err_msg, 'mock throw')
        self.assertEqual(N_str.children,
                         'Number of events: 0')

    def test_load_include(self):
        filters = {'peak_property': {'Amplitudes': 1.2}}
        filters['sample_log_filters'] = {}
        filters['time_filters'] = {'keep_filters': {'unit': [1, 2],
                                                    'test': [3, 4]},
                                   'remove_filters': {}}
        data, logs, state, headers = self.presenter.load(filters)
        self.assertEqual(state, 'Include')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name' + TT: 'unit',
                                   'Start' + TT: 1,
                                   'End' + TT: 2})
        self.assertEqual(data[1], {'Name' + TT: 'test',
                                   'Start' + TT: 3,
                                   'End' + TT: 4})
        self.assertEqual(logs, [])
        self.assertEqual(len(headers), 3)

    def test_load_exclude(self):
        filters = {'peak_property': {'Amplitudes': 1.2}}
        filters['sample_log_filters'] = {}
        filters['time_filters'] = {'keep_filters': {},
                                   'remove_filters': {'more': [5, 6],
                                                      'tests': [7, 8]}}
        data, logs, state, headers = self.presenter.load(filters)
        self.assertEqual(state, 'Exclude')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name' + TT: 'more',
                                   'Start' + TT: 5,
                                   'End' + TT: 6})
        self.assertEqual(data[1], {'Name' + TT: 'tests',
                                   'Start' + TT: 7,
                                   'End' + TT: 8})
        self.assertEqual(logs, [])
        self.assertEqual(len(headers), 3)

    def test_load_fail(self):
        filters = {'peak_property': {'Amplitudes': 1.2}}
        filters['sample_log_filters'] = []
        filters['time_filters'] = {'keep_filters': {'unit': [1, 2],
                                                    'test': [3, 4]},
                                   'remove_filters': {'more': [5, 6],
                                                      'tests': [7, 8]}}
        with self.assertRaises(RuntimeError):
            data, state = self.presenter.load(filters)

    def test_update_N_events_success(self):
        result = self.presenter.update_N_events(True, 'old')
        self.assertEqual(result, 'Number of events: Not Calculated')

    def test_update_N_events_failt(self):
        result = self.presenter.update_N_events(False, 'old')
        self.assertEqual(result, 'old')


if __name__ == '__main__':
    unittest.main()
