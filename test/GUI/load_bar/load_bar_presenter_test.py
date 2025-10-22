import unittest
from unittest import mock
from MuonDataLib.GUI.load_bar.presenter import LoadBarPresenter
from MuonDataLib.test_helpers.unit_test import TestHelper
import os


class LoadBarPresenterTest(TestHelper):

    @mock.patch("MuonDataLib.GUI.load_bar.presenter.LoadBarView")
    def setUp(self, view):
        self.view = view
        self.view.return_value = mock.Mock()
        self.load = LoadBarPresenter()

        self.file = os.path.join(os.path.dirname(__file__),
                                 '..',
                                 '..',
                                 'data_files',
                                 'HIFI00195790.nxs')

    def expected_report(self, result):
        expect = ("peak_property.Amplitudes: 3.14 \n"
                  "sample_log_filters.Temp: [0.0044, 0.163] \n"
                  "time_filters.keep_filters: {'first': [0.01, 0.02],"
                  " 'second': [0.05, 0.06]} \n"
                  "time_filters.remove_filters: {'one': [1, 2],"
                  " 'two': [5, 7]} \n")
        self.assertEqual(result, expect)

    def test_init(self):
        self.assertEqual(self.load._view,
                         self.view())
        # Check that the data is none
        self.assertEqual(self.load._data,
                         None)

    def test_load_nxs(self):
        self.load.load_nxs(self.file)

        self.assertEqual(self.load._data._dict['raw_data']._dict['run_number'],
                         195790)

    def test_load_filter(self):
        self.load.load_nxs(self.file)

        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'data_files',
                            'load_filter.json')
        result = self.load.load_filters(file)
        self.expected_report(result)

    @mock.patch("MuonDataLib.GUI.load_bar.presenter.load_events")
    def test_get_data(self, data_mock):
        data_mock.return_value = mock.Mock()
        self.load.load_nxs(self.file)
        self.assertEqual(self.load._data, data_mock())


if __name__ == '__main__':
    unittest.main()
