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


class FilterPresenterTest(TestHelper):

    def setUp(self):
        self.presenter = FilterPresenter()

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
                                     'Include')
        result = self.presenter._data.report_filters()

        expect = [0, {}, {}, {}]
        self.cf_filters(result, expect)

    def test_apply_filters_include(self):
        filters = [{'Name_t': 'unit',
                    'Start_t': 0.1,
                    'End_t': 0.5},
                   {'Name_t': 'test',
                    'Start_t': 0.7,
                    'End_t': 1.2}]

        self.presenter._data = load_events(FILE, 64)
        self.presenter.apply_filters(filters,
                                     'Include')
        result = self.presenter._data.report_filters()

        expect = [0,
                  {},
                  {'unit': [0.1, 0.5],
                   'test': [0.7, 1.2]},
                  {}]
        self.cf_filters(result, expect)

    def test_apply_filters_exclude(self):
        filters = [{'Name_t': 'unit',
                    'Start_t': 0.1,
                    'End_t': 0.5},
                   {'Name_t': 'test',
                    'Start_t': 0.7,
                    'End_t': 1.2}]

        self.presenter._data = load_events(FILE, 64)
        self.presenter.apply_filters(filters,
                                     'Exclude')
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
        clear = mock.Mock()
        self.presenter._data.clear_filters = clear
        N_str, err_msg = self.presenter.calculate(1, {}, 'Exclude')
        self.assertEqual(clear.call_count, 1)
        self.assertEqual(err_msg, '')
        self.assertEqual(N_str.children,
                         'Number of events: 64147')

    def test_calculate_with_exclude_filter(self):
        self.presenter._data = load_events(FILE, 64)
        clear = mock.Mock()
        self.presenter._data.clear_filters = clear
        filters = [{'Name_t': 'unit', 'Start_t': 0.1, 'End_t': 1.2}]
        N_str, err_msg = self.presenter.calculate(1, filters, 'Exclude')
        self.assertEqual(clear.call_count, 1)
        self.assertEqual(err_msg, '')
        self.assertEqual(N_str.children,
                         'Number of events: 57653')

    def test_calculate_with_include_filter(self):
        self.presenter._data = load_events(FILE, 64)
        clear = mock.Mock()
        self.presenter._data.clear_filters = clear
        filters = [{'Name_t': 'unit', 'Start_t': 0.1, 'End_t': 1.2}]
        N_str, err_msg = self.presenter.calculate(1, filters, 'Include')
        self.assertEqual(clear.call_count, 1)
        self.assertEqual(err_msg, '')
        self.assertEqual(N_str.children,
                         'Number of events: 5037')

    def test_calculate_with_error(self):
        def throw(filters, state):
            raise RuntimeError("mock throw")

        self.presenter._data = load_events(FILE, 64)
        clear = mock.Mock()
        self.presenter._data.clear_filters = clear
        self.presenter.apply_filters = mock.Mock(side_effect=throw)
        filters = [{'Name_t': 'unit', 'Start_t': 0.1, 'End_t': 1.2}]
        N_str, err_msg = self.presenter.calculate(1, filters, 'Include')
        self.assertEqual(clear.call_count, 1)
        self.assertEqual(err_msg, 'mock throw')
        self.assertEqual(N_str.children,
                         'Number of events: 0')

    def test_load_include(self):
        filters = {'peak_property': {'Amplitudes': 1.2}}
        filters['sample_log_filters'] = []
        filters['time_filters'] = {'keep_filters': {'unit': [1, 2],
                                                    'test': [3, 4]},
                                   'remove_filters': {}}
        data, state = self.presenter.load(filters)
        self.assertEqual(state, 'Include')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name_t': 'unit',
                                   'Start_t': 1,
                                   'End_t': 2})
        self.assertEqual(data[1], {'Name_t': 'test',
                                   'Start_t': 3,
                                   'End_t': 4})

    def test_load_exclude(self):
        filters = {'peak_property': {'Amplitudes': 1.2}}
        filters['sample_log_filters'] = []
        filters['time_filters'] = {'keep_filters': {},
                                   'remove_filters': {'more': [5, 6],
                                                      'tests': [7, 8]}}
        data, state = self.presenter.load(filters)
        self.assertEqual(state, 'Exclude')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name_t': 'more',
                                   'Start_t': 5,
                                   'End_t': 6})
        self.assertEqual(data[1], {'Name_t': 'tests',
                                   'Start_t': 7,
                                   'End_t': 8})

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
