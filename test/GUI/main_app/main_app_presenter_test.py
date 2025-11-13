import unittest
from unittest import mock
import os
import numpy as np

from MuonDataLib.GUI.main_app.presenter import MainAppPresenter
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.GUI.load_bar.view import CURRENT
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from data_paths import FILE, FILTER, EXPECT  # noqa: E402


"""
Only testing debug = False,
as it will removed in the long term
"""
DEBUG = False


class MainAppPresenterTest(TestHelper):

    @mock.patch("MuonDataLib.GUI.main_app.presenter.LoadBarPresenter")
    @mock.patch("MuonDataLib.GUI.main_app.presenter.FilterPresenter")
    @mock.patch("MuonDataLib.GUI.main_app.presenter.PlotAreaPresenter")
    @mock.patch("MuonDataLib.GUI.main_app.presenter.SaveBarPresenter")
    def test_init(self, save, plot, filters, load):

        load.return_value = mock.Mock()
        filters.return_value = mock.Mock()
        plot.return_value = mock.Mock()
        save.return_value = mock.Mock()

        MainAppPresenter()
        load.assert_called_once_with()
        filters.assert_called_once_with()
        plot.assert_called_once_with()
        save.assert_called_once_with()

    @mock.patch("MuonDataLib.GUI.main_app.presenter.PlotAreaPresenter")
    def test_load_nxs(self, plot):
        plt = mock.Mock()
        plt.plot = mock.Mock(return_value='plot')
        plot.return_value = plt

        app = MainAppPresenter()
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        result = app.load_nxs(CURRENT + FILE, DEBUG)

        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], '')

        self.assertMockOnce(plt.plot, [[1, 2, 3],
                                       [-1, 0, 1],
                                       [1, 2, 3],
                                       [-1, 0, 1]])

    @mock.patch("MuonDataLib.GUI.main_app.presenter.PlotAreaPresenter")
    def test_load_nxs_fails(self, plot):
        plt = mock.Mock()
        plt.plot = mock.Mock(return_value='plot')
        plot.return_value = plt

        app = MainAppPresenter()
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        bad_file = 'HIFI0.nxs'
        result = app.load_nxs(CURRENT + bad_file, DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1],
                         'An error occurred: '
                         'The file HIFI0.nxs cannot be read')

        self.assertMockOnce(plt.plot, [[],
                                       [],
                                       [],
                                       []])

    @mock.patch("MuonDataLib.GUI.main_app.presenter.PlotAreaPresenter")
    def test_load_nxs_none(self, plot):
        plt = mock.Mock()
        plt.plot = mock.Mock(return_value='plot')
        plot.return_value = plt

        app = MainAppPresenter()
        app.gen_fake_data = mock.Mock(return_value=(np.array([1., 2., 3.]),
                                                    np.array([-1., 0., 1.])))
        bad_file = 'None'
        result = app.load_nxs(CURRENT + bad_file, DEBUG)
        self.assertEqual(result[0], 'plot')
        self.assertEqual(result[1], '')

        self.assertMockOnce(plt.plot, [[],
                                       [],
                                       [],
                                       []])

    def test_load_filter(self):
        app = MainAppPresenter()
        _ = app.load_nxs(CURRENT + FILE, DEBUG)
        result = app.load_filter(CURRENT + FILTER, DEBUG)

        extra = "sample_log_filters.Test: [-0.2, -999.0] \n"
        pattern = 'time_filters.keep'
        tmp = EXPECT.split(pattern)
        txt = tmp[0] + extra + pattern + tmp[1]
        self.assertEqual(result[0], txt)
        self.assertEqual(result[1], '')

    def test_load_filter_fail(self):
        bad_file = 'filters.json'

        app = MainAppPresenter()
        _ = app.load_nxs(CURRENT + FILE, DEBUG)
        result = app.load_filter(CURRENT + bad_file, DEBUG)

        self.assertEqual(result[0], '')
        self.assertEqual(result[1], "Load filter error: "
                         "[Errno 2] No such file or "
                         f"directory: '{bad_file}'")

    def test_alert(self):

        app = MainAppPresenter()
        self.assertTrue(app.alert('error'))

    def test_alert_empty(self):

        app = MainAppPresenter()
        self.assertFalse(app.alert(''))

    def test_save_nxs(self):
        """
        Just check that a file is saved
        we assume its correct (covered
        by other unit tests).
        """
        app = MainAppPresenter()
        _ = app.load_nxs(CURRENT + FILE, DEBUG)
        dtype = 'n'
        file = 'test.nxs'
        name, msg = app.save_data(dtype + file, DEBUG)
        self.assertTrue(os.path.isfile(file))
        os.remove(file)
        self.assertEqual(name, file)
        self.assertEqual(msg, '')

    def test_save_json(self):
        app = MainAppPresenter()
        _ = app.load_nxs(CURRENT + FILE, DEBUG)
        dtype = 'j'
        file = 'test.json'
        name, msg = app.save_data(dtype + file, DEBUG)

        self.assertTrue(os.path.isfile(file))
        os.remove(file)
        self.assertEqual(name, file)
        self.assertEqual(msg, '')

    def test_save_error(self):
        app = MainAppPresenter()
        _ = app.load_nxs(CURRENT + FILE, DEBUG)
        dtype = 'j'
        file = 'test.json'

        def throw(name):
            raise RuntimeError("save crash")

        app._data.save_filters = mock.Mock(side_effect=throw)

        name, msg = app.save_data(dtype + file, DEBUG)
        self.assertFalse(os.path.isfile(file))
        self.assertEqual(name, '')
        self.assertEqual(str(msg), 'Saving Error: save crash')

    def test_save_none(self):
        app = MainAppPresenter()
        result = app.save_data('None', DEBUG)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], '')


if __name__ == '__main__':
    unittest.main()
