import unittest
from unittest import mock
import os
import numpy as np
import h5py
import json

from MuonDataLib.GUI.main_app.presenter import MainAppPresenter
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.GUI.load_bar.view import CURRENT
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from data_paths import FILE, FILTER, BADFILTER  # noqa: E402


"""
Only testing debug = False,
as it will removed in the long term
"""
DEBUG = False


def dummy_open(N_clicks):
    return 'bob.nxs'


class MainAppPresenterTest(TestHelper):

    @mock.patch("MuonDataLib.GUI.main_app.presenter.LoadBarPresenter")
    @mock.patch("MuonDataLib.GUI.main_app.presenter.ControlPanePresenter")
    @mock.patch("MuonDataLib.GUI.main_app.presenter.SaveBarPresenter")
    def test_init(self, save, control, load):

        load.return_value = mock.Mock()
        control.return_value = mock.Mock()
        save.return_value = mock.Mock()

        _ = MainAppPresenter(dummy_open)

        load.assert_called_once_with()
        control.assert_called_once_with()
        save.assert_called_once_with()

    def test_open_nxs(self):
        mock_open = mock.Mock(return_value='bob.nxs')
        app = MainAppPresenter(mock_open)
        new_name = app.open_nxs(1, 'old.nxs')

        self.assertEqual(new_name, 'bob.nxs')
        mock_open.assert_called_once_with(1)

    def test_open_nxs_no_update(self):
        mock_open = mock.Mock(return_value='bob.nxs')
        app = MainAppPresenter(mock_open)
        new_name = app.open_nxs(0, 'old.nxs')

        self.assertEqual(new_name, 'old.nxs')
        mock_open.assert_not_called()

    def test_confirm_load_no_filters(self):
        app = MainAppPresenter(dummy_open)
        state, clicks = app.confirm_load(2, {}, 1)
        self.assertFalse(state)
        self.assertEqual(clicks, 2)

    def test_confirm_load_with_filters(self):
        app = MainAppPresenter(dummy_open)
        filters = {'Name_t': 'test',
                   'Start_t': 1,
                   'End_t': 3}
        state, clicks = app.confirm_load(2, filters, 1)
        self.assertTrue(state)
        self.assertEqual(clicks, i
    def test_confirm_load_no_filters(self):
        app = MainAppPresenter(dummy_open)
        state, clicks = app.confirm_load(2, {}, 1)
        self.assertFalse(state)
        self.assertEqual(clicks, 2)

)

    def test_load_nxs(self):

        app = MainAppPresenter(dummy_open)
        app.plot = mock.Mock(return_value='plot')

        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        result = app.load_nxs(CURRENT + FILE, [], DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], '')

        self.assertMockOnce(app.plot, [[1, 2, 3],
                                       [-1, 0, 1],
                                       [1, 2, 3],
                                       [-1, 0, 1]])

    def test_load_nxs_fails(self):

        app = MainAppPresenter(dummy_open)
        app.plot = mock.Mock(return_value='plot')
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        bad_file = 'HIFI0.nxs'
        result = app.load_nxs(CURRENT + bad_file, [], DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2],
                         'An error occurred: '
                         'The file HIFI0.nxs cannot be read')

        self.assertMockOnce(app.plot, [[],
                                       [],
                                       [],
                                       []])

    def test_load_nxs_none(self):
        app = MainAppPresenter(dummy_open)
        app.plot = mock.Mock(return_value='plot')
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        bad_file = 'None'
        result = app.load_nxs(CURRENT + bad_file, [], DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], '')

        self.assertMockOnce(app.plot, [[],
                                       [],
                                       [],
                                       []])

    def test_load_nxs_with_filters(self):

        app = MainAppPresenter(dummy_open)
        app.plot = mock.Mock(return_value='plot')

        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        filters = [{'Name': 'test', 'Start': 0, 'End': 1}]
        result = app.load_nxs(CURRENT + FILE, filters, DEBUG)
        self.assertEqual(result[0], 'plot')
        # should clear the filters
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], '')

        self.assertMockOnce(app.plot, [[1, 2, 3],
                                       [-1, 0, 1],
                                       [1, 2, 3],
                                       [-1, 0, 1]])

    def test_load_nxs_fails_with_filters(self):

        app = MainAppPresenter(dummy_open)
        app.plot = mock.Mock(return_value='plot')
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        bad_file = 'HIFI0.nxs'
        filters = [{'Name': 'test', 'Start': 0, 'End': 1}]
        result = app.load_nxs(CURRENT + bad_file, filters, DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2],
                         'An error occurred: '
                         'The file HIFI0.nxs cannot be read')

        self.assertMockOnce(app.plot, [[],
                                       [],
                                       [],
                                       []])

    def test_load_nxs_none_with_filters(self):
        app = MainAppPresenter(dummy_open)
        app.plot = mock.Mock(return_value='plot')
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        bad_file = 'None'
        filters = [{'Name': 'test', 'Start': 0, 'End': 1}]
        result = app.load_nxs(CURRENT + bad_file, filters, DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], '')

        self.assertMockOnce(app.plot, [[],
                                       [],
                                       [],
                                       []])

    def test_load_filter_time_fails(self):
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        result = app.load_filter(CURRENT + BADFILTER, DEBUG)

        self.assertEqual(result[0], '')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], 'Exclude')
        self.assertEqual(result[3], 'Load filter error: Cannot have '
                         'both include and exclude time filters')

    def test_load_filter(self):
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        result = app.load_filter(CURRENT + FILTER, DEBUG)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], [{'Name_t': 'first',
                                      'Start_t': 0.01,
                                      'End_t': 0.02},
                                     {'Name_t': 'second',
                                      'Start_t': 0.05,
                                      'End_t': 0.06},
                                     ])
        self.assertEqual(result[2], 'Include')
        self.assertEqual(result[3], '')

    def test_load_filter_fail(self):
        bad_file = 'filters.json'

        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        result = app.load_filter(CURRENT + bad_file, DEBUG)

        self.assertEqual(result[0], '')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], 'Exclude')
        self.assertEqual(result[3], "Load filter error: "
                         "[Errno 2] No such file or "
                         f"directory: '{bad_file}'")

    def test_load_filter_with_filter_table(self):
        app = MainAppPresenter(dummy_open)
        filters = [{'Name': 'test', 'Start': 0, 'End': 1}]
        _ = app.load_nxs(CURRENT + FILE, filters, DEBUG)
        result = app.load_filter(CURRENT + FILTER, DEBUG)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], [{'Name_t': 'first',
                                      'Start_t': 0.01,
                                      'End_t': 0.02},
                                     {'Name_t': 'second',
                                      'Start_t': 0.05,
                                      'End_t': 0.06},
                                     ])
        self.assertEqual(result[2], 'Include')
        self.assertEqual(result[3], '')

    def test_load_filter_fail_with_filter_table(self):
        bad_file = 'filters.json'

        app = MainAppPresenter(dummy_open)
        filters = [{'Name': 'test', 'Start': 0, 'End': 1}]
        _ = app.load_nxs(CURRENT + FILE, filters, DEBUG)
        result = app.load_filter(CURRENT + bad_file, DEBUG)

        self.assertEqual(result[0], '')
        self.assertEqual(result[1], [])
        self.assertEqual(result[2], 'Exclude')
        self.assertEqual(result[3], "Load filter error: "
                         "[Errno 2] No such file or "
                         f"directory: '{bad_file}'")

    def test_alert(self):

        app = MainAppPresenter(dummy_open)
        self.assertTrue(app.alert('error'))

    def test_alert_empty(self):

        app = MainAppPresenter(dummy_open)
        self.assertFalse(app.alert(''))

    def test_save_nxs(self):
        """
        Just check that a file is saved
        we assume its correct (covered
        by other unit tests).
        """
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        dtype = 'n'
        file_name = 'test.nxs'
        name, msg = app.save_data(dtype + file_name, [], 'Exclude', DEBUG)
        self.assertTrue(os.path.isfile(file_name))

        with h5py.File(file_name, 'r') as file:
            tmp = file['raw_data_1']['instrument']['detector_1']
            hist = tmp['counts']
            self.assertEqual(np.sum(hist), 64147)

        os.remove(file_name)
        self.assertEqual(name, file_name)
        self.assertEqual(msg, '')

    def test_save_nxs_with_exclude_filter(self):
        """
        Just check that a file is saved
        we assume its correct (covered
        by other unit tests).
        """
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        dtype = 'n'
        file_name = 'test.nxs'
        filters = [{'Name_t': 'unit', 'Start_t': 1.2, 'End_t': 200}]
        name, msg = app.save_data(dtype + file_name, filters, 'Exclude', DEBUG)
        self.assertTrue(os.path.isfile(file_name))

        with h5py.File(file_name, 'r') as file:
            tmp = file['raw_data_1']['instrument']['detector_1']
            hist = tmp['counts']
            self.assertEqual(np.sum(hist), 5755)

        os.remove(file_name)
        self.assertEqual(name, file_name)
        self.assertEqual(msg, '')

    def test_save_nxs_with_include_filter(self):
        """
        Just check that a file is saved
        we assume its correct (covered
        by other unit tests).
        """
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        dtype = 'n'
        file_name = 'test.nxs'
        filters = [{'Name_t': 'unit', 'Start_t': 1.2, 'End_t': 100},
                   {'Name_t': 'test', 'Start_t': 150, 'End_t': 200}]
        name, msg = app.save_data(dtype + file_name, filters, 'Include', DEBUG)
        self.assertTrue(os.path.isfile(file_name))

        with h5py.File(file_name, 'r') as file:
            tmp = file['raw_data_1']['instrument']['detector_1']
            hist = tmp['counts']
            self.assertEqual(np.sum(hist), 56895)

        os.remove(file_name)
        self.assertEqual(name, file_name)
        self.assertEqual(msg, '')

    def test_save_json_Exclude(self):
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        dtype = 'j'
        file = 'test.json'
        filters = [{'Name_t': 'unit_test', 'Start_t': 1.2, 'End_t': 200}]
        name, msg = app.save_data(dtype + file, filters, 'Exclude', DEBUG)

        with open('test.json') as f:
            result = json.load(f)
        self.assertEqual(len(result), 3)

        self.assertEqual(result['peak_property']['Amplitudes'], 0.0)
        self.assertEqual(result['sample_log_filters'], {})
        self.assertEqual(result['time_filters']['keep_filters'], {})
        self.assertEqual(result['time_filters']['remove_filters'],
                         {'unit_test': [1.2, 200]})

        self.assertTrue(os.path.isfile(file))
        os.remove(file)
        self.assertEqual(name, file)
        self.assertEqual(msg, '')

    def test_save_json_Include(self):
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        dtype = 'j'
        file = 'test.json'
        filters = [{'Name_t': 'unit_test', 'Start_t': 1.2, 'End_t': 200}]
        name, msg = app.save_data(dtype + file, filters, 'Include', DEBUG)

        with open('test.json') as f:
            result = json.load(f)
        self.assertEqual(len(result), 3)

        self.assertEqual(result['peak_property']['Amplitudes'], 0.0)
        self.assertEqual(result['sample_log_filters'], {})
        self.assertEqual(result['time_filters']['keep_filters'],
                         {'unit_test': [1.2, 200]})
        self.assertEqual(result['time_filters']['remove_filters'], {})

        self.assertTrue(os.path.isfile(file))
        os.remove(file)
        self.assertEqual(name, file)
        self.assertEqual(msg, '')

    def test_save_filter_error(self):
        app = MainAppPresenter(dummy_open)
        _ = app.load_nxs(CURRENT + FILE, [], DEBUG)
        dtype = 'j'
        file = 'test.json'

        def throw(name):
            raise RuntimeError("save crash")

        app.load._data.save_filters = mock.Mock(side_effect=throw)

        name, msg = app.save_data(dtype + file, [], ' Exclude', DEBUG)
        self.assertFalse(os.path.isfile(file))
        self.assertEqual(name, '')
        self.assertEqual(str(msg), 'Saving Error: save crash')

    def test_save_none(self):
        app = MainAppPresenter(dummy_open)
        result = app.save_data('None', [], 'Exclude', DEBUG)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], '')


if __name__ == '__main__':
    unittest.main()
