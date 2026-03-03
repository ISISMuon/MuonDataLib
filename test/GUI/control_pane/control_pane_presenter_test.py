import unittest
from unittest import mock
from MuonDataLib.GUI.control_pane.presenter import ControlPanePresenter
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.data.loader.load_events import load_events
import sys
import os
from dash import no_update
import numpy as np

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from data_paths import FILTER  # noqa: E402


TT = '_time-table'
LT = '_log-table'


class ControlPanePresenterTest(TestHelper):

    def setUp(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        self.data = load_events(file, 64)
        # add some extra sample logs
        x, _ = self.data._get_sample_log('Temp').get_values()
        self.data.add_sample_log('B', x, np.cos(.2*x))
        self.data.add_sample_log('I', x, np.exp(-0.2*x))

        self.presenter = ControlPanePresenter()
        self.presenter.set_data(self.data)
        # just add a plot
        log_table = [{'sample_log-table': 'Temp'},
                     {'sample_log-table': 'B'}]
        self.presenter.make_plot([], log_table, 'Exclude')

    @property
    def get_fig(self):
        return self.presenter._plot.fig

    @property
    def logs(self):
        return self.data._dict['logs']

    def test_clear(self):
        self.presenter._filter._log._logs = 'logs'
        self.presenter._filter._data = 'data'

        self.presenter.clear()
        self.assertEqual(self.presenter._filter._log._logs, None)
        self.assertEqual(self.presenter._filter._data, None)

    def test_empty(self):
        self.presenter._plot.plot = mock.Mock()
        self.presenter.empty()

        self.assertMockOnce(self.presenter._plot.plot,
                            [[''],
                             [[1]],
                             [[1]]])

    def test_plot_default(self):
        self.presenter._filter._log.get_new_log_name = mock.Mock()
        self.presenter._filter._log.get_new_log_name.return_value = 'I'
        self.presenter._plot.new_plot = mock.Mock()
        mock_logs = mock.Mock()
        self.presenter._filter._log._logs = mock_logs

        self.presenter.plot_default()
        self.presenter._plot.new_plot.assert_called_once_with(['I'],
                                                              mock_logs)

    def test_plot_default_empty(self):
        self.presenter._plot.plot = mock.Mock()
        self.presenter.clear()

        self.presenter.plot_default()
        self.assertMockOnce(self.presenter._plot.plot,
                            [[''],
                             [[1]],
                             [[1]]])

    def test_make_plot_empty_data(self):
        self.presenter._plot.plot = mock.Mock()
        self.presenter.clear()

        self.presenter.make_plot([], [], 'Exclude')
        self.assertMockOnce(self.presenter._plot.plot,
                            [[''],
                             [[1]],
                             [[1]]])

    def test_make_plot_empty_filters(self):
        self.presenter._plot.new_plot = mock.Mock()
        self.presenter.add_time_filters = mock.Mock()

        self.presenter.make_plot([], [], 'Exclude')

        self.presenter._plot.new_plot  .assert_called_once_with(['Temp'],
                                                                self.logs)
        self.presenter.add_time_filters.assert_called_once_with([], 'Exclude')

    def test_make_plot_one_log(self):
        self.presenter._plot.new_plot = mock.Mock()
        self.presenter.add_time_filters = mock.Mock()

        self.presenter.make_plot([], [{'sample_log-table': 'B'}], 'Exclude')

        self.presenter._plot.new_plot  .assert_called_once_with(['B'],
                                                                self.logs)
        self.presenter.add_time_filters.assert_called_once_with([], 'Exclude')

    def test_make_plot_two_logs(self):
        self.presenter._plot.new_plot = mock.Mock()
        self.presenter.add_time_filters = mock.Mock()

        self.presenter.make_plot([], [{'sample_log-table': 'B'},
                                      {'sample_log-table': 'I'}], 'Exclude')

        self.presenter._plot.new_plot  .assert_called_once_with(['B', 'I'],
                                                                self.logs)
        self.presenter.add_time_filters.assert_called_once_with([], 'Exclude')

    def test_make_plot_two_logs_and_time(self):
        self.presenter._plot.new_plot = mock.Mock()
        self.presenter.add_time_filters = mock.Mock()

        self.presenter.make_plot([{'time': 1}], [{'sample_log-table': 'B'},
                                                 {'sample_log-table': 'I'}],
                                 'Exclude')

        self.presenter._plot.new_plot  .assert_called_once_with(['B', 'I'],
                                                                self.logs)
        self.presenter.add_time_filters.assert_called_once_with([{'time': 1}],
                                                                'Exclude')

    def test_add_filter_include(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 4, 0, 1],
                           ])

        self.presenter.add_time_filters([{'Name' + TT: 'unit',
                                          'Start' + TT: 0.2,
                                          'End' + TT: 0.4},
                                         {'Name' + TT: 'test',
                                          'Start' + TT: 0.7,
                                          'End' + TT: 0.8}],
                                        'Include')
        self.check_shapes([[0.2, 0.4, 0, 1],
                           [0.7, 0.8, 0, 1],
                           ])

    def test_add_filter_exclude(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 4, 0, 1],
                           ])

        self.presenter.add_time_filters([{'Name' + TT: 'unit',
                                          'Start' + TT: 0.2,
                                          'End' + TT: 0.4},
                                         {'Name' + TT: 'test',
                                          'Start' + TT: 0.7,
                                          'End' + TT: 0.8}],
                                        'Exclude')

        self.check_shapes([[0.0, 0.2, 0, 1],
                           [0.4, 0.7, 0, 1],
                           [0.8, 4.0, 0, 1],
                           ])

    def test_add_filter_include_empty(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 4, 0, 1],
                           ])

        self.presenter.add_time_filters([], 'Include')

        self.check_shapes([])

    def test_add_filter_exclude_empty(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 4, 0, 1],
                           ])

        self.presenter.add_time_filters([],
                                        'Exclude')

        self.check_shapes([[0, 4, 0, 1]])

    def test_apply_exc_data_empty(self):
        shade = mock.Mock()
        self.presenter._plot.add_shaded_region = shade
        self.presenter.apply_exc_data([], [])
        self.assertEqual(shade.call_count,
                         0)

    def test_apply_exc_data_one(self):
        shade = mock.Mock()
        self.presenter._plot.add_shaded_region = shade
        self.presenter.apply_exc_data([.1], [.3])
        self.assertEqual(shade.call_count,
                         2)
        shade.assert_any_call(0, .1)
        shade.assert_any_call(0.3, 4.)

    def test_apply_exc_data_multiple(self):
        shade = mock.Mock()
        self.presenter._plot.add_shaded_region = shade
        self.presenter.apply_exc_data([.1, .3], [.2, .4])
        self.assertEqual(shade.call_count,
                         3)
        shade.assert_any_call(0, .1)
        shade.assert_any_call(0.2, .3)
        shade.assert_any_call(0.4, 4.)

    def test_set_data(self):
        reset = mock.Mock()
        self.presenter._plot.reset_plot_range = reset
        data = mock.Mock()
        data.get_frame_start_times = mock.Mock(return_value=[0.1, 3, 6, 11])
        data._dict = {'logs': 'log data'}

        self.presenter.set_data(data)

        self.assertEqual(reset.call_count, 1)
        self.assertEqual(self.presenter._filter._data,
                         data)
        self.assertEqual(self.presenter._filter._log._logs,
                         'log data')

    def test_display_hover_None(self):
        result = self.presenter.display_hover(None,
                                              {},
                                              'Include')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], no_update)
        self.assertEqual(result[2], no_update)

    def test_headers(self):
        # just check the number of header groups
        self.assertEqual(len(self.presenter.headers), 3)

    def check_hover_text(self, hover, expect):

        # loop over html objects for the tooltip
        for k, child in enumerate(hover.children):
            self.assertEqual(child.children,
                             expect[k])

    def test_display_hover_include_not_over_shaded(self):
        hover = {}
        hover['points'] = [{'bbox': [1, 2, 3, 4],
                            'x': 0.2,
                            'y': 0.5}]
        filters = [{'Name' + TT: 'test',
                    'Start' + TT: 0.4,
                    'End' + TT: 0.6}]

        result = self.presenter.display_hover(hover,
                                              filters,
                                              'Include')
        self.assertEqual(result[0], True)
        self.assertArrays(result[1], [1, 2, 3, 4])

        expect = ['Data Point',
                  'x: 0.200,  y: 0.500',
                  'Status',
                  'Keep data: False']
        self.check_hover_text(result[2], expect)

    def test_display_hover_include_over_shaded(self):
        hover = {}
        hover['points'] = [{'bbox': [1, 2, 3, 4],
                            'x': 0.5,
                            'y': 0.5}]
        filters = [{'Name' + TT: 'test',
                    'Start' + TT: 0.4,
                    'End' + TT: 0.6}]

        result = self.presenter.display_hover(hover,
                                              filters,
                                              'Include')
        self.assertEqual(result[0], True)
        self.assertArrays(result[1], [1, 2, 3, 4])

        expect = ['Data Point',
                  'x: 0.500,  y: 0.500',
                  'Status',
                  'Keep data: True. Added by: test, ']
        self.check_hover_text(result[2], expect)

    def test_display_hover_include_over_shaded_2(self):
        hover = {}
        hover['points'] = [{'bbox': [1, 2, 3, 4],
                            'x': 0.5,
                            'y': 0.5}]
        filters = [{'Name' + TT: 'unit',
                    'Start' + TT: 0.4,
                    'End' + TT: 0.6},
                   {'Name' + TT: 'test',
                    'Start' + TT: 0.2,
                    'End' + TT: 0.7},
                   ]

        result = self.presenter.display_hover(hover,
                                              filters,
                                              'Include')
        self.assertEqual(result[0], True)
        self.assertArrays(result[1], [1, 2, 3, 4])

        expect = ['Data Point',
                  'x: 0.500,  y: 0.500',
                  'Status',
                  'Keep data: True. Added by: unit, test, ']
        self.check_hover_text(result[2], expect)

    def test_display_hover_exclude_not_over_shaded(self):
        hover = {}
        hover['points'] = [{'bbox': [1, 2, 3, 4],
                            'x': 0.5,
                            'y': 0.5}]
        filters = [{'Name' + TT: 'test',
                    'Start' + TT: 0.4,
                    'End' + TT: 0.6}]

        result = self.presenter.display_hover(hover,
                                              filters,
                                              'Exclude')
        self.assertEqual(result[0], True)
        self.assertArrays(result[1], [1, 2, 3, 4])

        expect = ['Data Point',
                  'x: 0.500,  y: 0.500',
                  'Status',
                  'Keep data: False. Removed by: test, ']
        self.check_hover_text(result[2], expect)

    def test_display_hover_exclude_over_shaded(self):
        hover = {}
        hover['points'] = [{'bbox': [1, 2, 3, 4],
                            'x': 0.2,
                            'y': 0.5}]
        filters = [{'Name' + TT: 'test',
                    'Start' + TT: 0.4,
                    'End' + TT: 0.6}]

        result = self.presenter.display_hover(hover,
                                              filters,
                                              'Exclude')
        self.assertEqual(result[0], True)
        self.assertArrays(result[1], [1, 2, 3, 4])

        expect = ['Data Point',
                  'x: 0.200,  y: 0.500',
                  'Status',
                  'Keep data: True']
        self.check_hover_text(result[2], expect)

    def test_display_hover_exclude_not_over_shaded_2(self):
        hover = {}
        hover['points'] = [{'bbox': [1, 2, 3, 4],
                            'x': 0.5,
                            'y': 0.5}]
        filters = [{'Name' + TT: 'unit',
                    'Start' + TT: 0.4,
                    'End' + TT: 0.6},
                   {'Name' + TT: 'test',
                    'Start' + TT: 0.2,
                    'End' + TT: 0.7},
                   ]

        result = self.presenter.display_hover(hover,
                                              filters,
                                              'Exclude')
        self.assertEqual(result[0], True)
        self.assertArrays(result[1], [1, 2, 3, 4])

        expect = ['Data Point',
                  'x: 0.500,  y: 0.500',
                  'Status',
                  'Keep data: False. Removed by: unit, test, ']
        self.check_hover_text(result[2], expect)

    def test_read_filter(self):
        data, state, cols = self.presenter.read_filter(FILTER)
        self.assertEqual(state, 'Include')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name' + TT: 'first',
                                   'Start' + TT: 0.01,
                                   'End' + TT: 0.02})
        self.assertEqual(data[1], {'Name' + TT: 'second',
                                   'Start' + TT: 0.05,
                                   'End' + TT: 0.06})
        # this is the only bit that can change
        self.assertEqual(cols[2]['headerName'], 'Include Filter details')


if __name__ == '__main__':
    unittest.main()
