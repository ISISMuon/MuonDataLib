import unittest
from unittest import mock
import os
import time
from MuonDataLib.cython_ext.load_events import load_data, _load_data
from MuonDataLib.test_helpers.unit_test import TestHelper


class LoadEventDataTest(TestHelper):

    def assertLongArrays(self, result, indicies, expected_len, ref):
        self.assertEqual(len(result), expected_len)
        self.assertArrays(result[indicies], ref)

    def test__load_data(self):
        """
        """
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'simple_test.nxs')
        IDs, start_j, times, amps, start_t, periods = _load_data(file)

        self.assertLongArrays(IDs, [1, 2, 3, 2122, 4000], 4060,
                              [0, 0, 1, 4, 60])
        self.assertArrays(start_j, [0, 252, 685, 1289, 2055, 2982])
        self.assertLongArrays(times, [1, 2, 3, 2122, 4000], 4060,
                              [602., 3846., 430., 2887., 1566.0])
        self.assertLongArrays(amps, [1, 2, 3, 2122, 4000], 4060,
                              [10., 10., 10., 10., 10.0])
        self.assertArrays(start_t, [0, 2e7, 4e7, 6e7, 8e7, 1e8])
        self.assertArrays(periods, [0, 0, 0, 0, 0, 0])

    def test__load_data_multiperiod(self):
        """
        """
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        IDs, start_j, times, amps, start_t, periods = _load_data(file)

        indices = [1, 2, 3, 50, 52, 79]

        self.assertLongArrays(periods, indices, 88,
                              [0, 0, 0, 1, 1, 1])

        self.assertLongArrays(IDs, indices, 64147,
                              [56, 56, 56, 60, 60, 32])
        self.assertLongArrays(start_j, indices, 88,
                              [718, 1472, 2219, 36036, 37525, 57445])
        self.assertLongArrays(times, indices, 64147,
                              [454., 592., 657., 1810., 3329., 3900.])
        self.assertLongArrays(amps, indices, 64147,
                              [2102., 2225., 2149., 2324., 2280., 2377.])
        self.assertLongArrays(start_t/1.e9, indices, 88,
                              [1.014, 1.054, 1.074, 2.254, 2.294, 2.974])

    @mock.patch('MuonDataLib.cython_ext.load_events._load_data')
    @mock.patch('MuonDataLib.cython_ext.load_events.Events')
    def test_load_data(self, events_mock, load_mock):
        """
        For this we are going to mock most of the computation,
        as the individual parts are tested.
        This will save on runtime for the test.
        Hence, this test can focus on
        checking the corret order of operations
        and the correct arguments are passed.
        """
        IDs = [0, 1, 0, 1]
        start_j = [0, 2]
        times = [0, .1, .2, .3]
        amps = [4, 5, 6]
        start_t = [0, 2]
        periods = [0, 0]

        def fake_load(file_name):
            # add a sleep so we can test the timer
            time.sleep(1.0)
            return IDs, start_j, times, amps, start_t, periods

        events_mock.return_value = mock.Mock()
        load_mock.side_effect = fake_load
        time_taken, events = load_data('test.nxs', 2)
        load_mock.assert_called_once_with("test.nxs")
        self.assertGreater(time_taken, 0.99)
        events_mock.assert_called_once_with(IDs, times, start_j,
                                            start_t, 2, periods)


if __name__ == '__main__':
    unittest.main()
