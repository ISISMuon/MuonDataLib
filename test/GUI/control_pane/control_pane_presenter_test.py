import unittest
from unittest import mock
from MuonDataLib.GUI.control_pane.presenter import ControlPanePresenter
from MuonDataLib.test_helpers.unit_test import TestHelper
import sys
import os
from dash import no_update


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from data_paths import FILTER  # noqa: E402


class ControlPanePresenterTest(TestHelper):

    def setUp(self):
        self.presenter = ControlPanePresenter()
        # just add a plot
        self.presenter._plot.plot([0], [1], [2], [2])

    def test_add_filter_include(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 2, 0, 1],
                           ])

        self.presenter.add_filter([{'Name_t': 'unit',
                                    'Start_t': 0.2,
                                    'End_t': 0.4},
                                   {'Name_t': 'test',
                                    'Start_t': 0.7,
                                    'End_t': 0.8}],
                                  'Include')

        self.check_shapes([[0.2, 0.4, 0, 1],
                           [0.7, 0.8, 0, 1],
                           ])

    def test_add_filter_exclude(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 2, 0, 1],
                           ])

        self.presenter.add_filter([{'Name_t': 'unit',
                                    'Start_t': 0.2,
                                    'End_t': 0.4},
                                   {'Name_t': 'test',
                                    'Start_t': 0.7,
                                    'End_t': 0.8}],
                                  'Exclude')

        self.check_shapes([[0.0, 0.2, 0, 1],
                           [0.4, 0.7, 0, 1],
                           [0.8, 2.0, 0, 1],
                           ])

    def test_add_filter_include_empty(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 2, 0, 1],
                           ])

        self.presenter.add_filter([], 'Include')

        self.check_shapes([])

    def test_add_filter_exclude_empty(self):
        # by default should have 2 shapes that cover both plots
        self.check_shapes([[0, 2, 0, 1],
                           ])

        self.presenter.add_filter([],
                                  'Exclude')

        self.check_shapes([[0, 2, 0, 1]])

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
        shade.assert_any_call(0.3, 2.)

    def test_apply_exc_data_multiple(self):
        shade = mock.Mock()
        self.presenter._plot.add_shaded_region = shade
        self.presenter.apply_exc_data([.1, .3], [.2, .4])
        self.assertEqual(shade.call_count,
                         3)
        shade.assert_any_call(0, .1)
        shade.assert_any_call(0.2, .3)
        shade.assert_any_call(0.4, 2.)

    def test_set_data(self):
        reset = mock.Mock()
        self.presenter._plot.reset_plot_range = reset
        data = mock.Mock()

        self.presenter.set_data(data)
        self.assertEqual(reset.call_count, 1)
        self.assertEqual(self.presenter._filter._data,
                         data)

    def test_display_hover_None(self):
        result = self.presenter.display_hover(None,
                                              {},
                                              'Include')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], no_update)
        self.assertEqual(result[2], no_update)

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
        filters = [{'Name_t': 'test',
                    'Start_t': 0.4,
                    'End_t': 0.6}]

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
        filters = [{'Name_t': 'test',
                    'Start_t': 0.4,
                    'End_t': 0.6}]

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
        filters = [{'Name_t': 'unit',
                    'Start_t': 0.4,
                    'End_t': 0.6},
                   {'Name_t': 'test',
                    'Start_t': 0.2,
                    'End_t': 0.7},
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
        filters = [{'Name_t': 'test',
                    'Start_t': 0.4,
                    'End_t': 0.6}]

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
        filters = [{'Name_t': 'test',
                    'Start_t': 0.4,
                    'End_t': 0.6}]

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
        filters = [{'Name_t': 'unit',
                    'Start_t': 0.4,
                    'End_t': 0.6},
                   {'Name_t': 'test',
                    'Start_t': 0.2,
                    'End_t': 0.7},
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
        data, state = self.presenter.read_filter(FILTER)
        self.assertEqual(state, 'Include')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {'Name_t': 'first',
                                   'Start_t': 0.01,
                                   'End_t': 0.02})
        self.assertEqual(data[1], {'Name_t': 'second',
                                   'Start_t': 0.05,
                                   'End_t': 0.06})


if __name__ == '__main__':
    unittest.main()
