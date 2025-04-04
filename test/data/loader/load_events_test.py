from MuonDataLib.data.loader.load_events import (load_log_data,
                                                 load_logs,
                                                 load_events)
from MuonDataLib.test_helpers.unit_test import TestHelper
import unittest
from unittest import mock
import os
import h5py
import numpy as np


FILENAME = 'load_events.nxs'


class mock_data(object):
    def __init__(self):
        """
        This is a simple class for testing the
        reading of the sample log data.
        It just stores sample log data.
        """
        self.dict = {}

    def add_sample_log(self, name, x, y):
        """
        This mocks the interface for the muondata
        class, when adding sample logs.
        :param name: the name of the log
        :param x: the x values
        :param y: the y values
        """
        self.dict[name] = (x, y)


class LoadEventsTest(TestHelper):

    def test_load_with_logs(self):
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'data_files',
                            'HIFI00195790.nxs')
        data = load_events(file, 64)
        log = data._get_sample_log('Temp')
        x, y = log.get_values()
        self.assertArrays(x, np.asarray([0, 1, 2, 3, 4], dtype=np.double))
        self.assertArrays(y, np.asarray([39, 36, 36, 37, 35], dtype=np.double))

    def test_load_log_data(self):
        # create nxs file with just sample logs
        file = h5py.File(FILENAME, 'w')
        group = file.require_group('Temp')
        group = group.require_group('value_log')
        group.require_dataset('time',
                              shape=(2),
                              data=np.asarray([1, 2],
                                              dtype=np.float32),
                              dtype=np.float32)
        group.require_dataset('value',
                              shape=(2),
                              data=np.asarray([3, 4],
                                              dtype=np.float32),
                              dtype=np.float32)
        file.close()

        # test that we can read the file
        data = mock_data()
        with h5py.File(FILENAME, 'r') as file:
            load_log_data(file['Temp'], 'Temp', data)
        self.assertEqual(len(data.dict), 1)
        x, y = data.dict['Temp']
        self.assertArrays(x, np.asarray([1, 2], dtype=np.double))
        self.assertArrays(y, np.asarray([3, 4], dtype=np.double))
        os.remove(FILENAME)

    def test_load_log_data_bad_values_ints(self):
        # create nxs file with just sample log data
        file = h5py.File(FILENAME, 'w')
        group = file.require_group('Temp')
        group = group.require_group('value_log')
        group.require_dataset('time',
                              shape=(2),
                              data=np.asarray([1, 2],
                                              dtype=np.int32),
                              dtype=np.int32)
        group.require_dataset('value',
                              shape=(2),
                              data=np.asarray([3, 4],
                                              dtype=np.float32),
                              dtype=np.float32)
        file.close()

        # test that we can read the file
        data = mock_data()
        with h5py.File(FILENAME, 'r') as file:
            load_log_data(file['Temp'], 'Temp', data)
        self.assertEqual(len(data.dict), 0)
        os.remove(FILENAME)

    def test_load_logs(self):
        # create nxs file with just sample log data
        file = h5py.File(FILENAME, 'w')
        log = file.require_group('Temp')
        log = log.require_group('value_log')
        log.require_dataset('time',
                            shape=(2),
                            data=np.asarray([1, 2],
                                            dtype=np.float32),
                            dtype=np.float32)
        log.require_dataset('value',
                            shape=(2),
                            data=np.asarray([3, 4],
                                            dtype=np.float32),
                            dtype=np.float32)

        log = file.require_group('field')
        log = log.require_group('value_log')
        log.require_dataset('time',
                            shape=(2),
                            data=np.asarray([1.2, 2.2],
                                            dtype=np.float32),
                            dtype=np.float32)
        log.require_dataset('value',
                            shape=(2),
                            data=np.asarray([6, 8],
                                            dtype=np.float32),
                            dtype=np.float32)

        file.close()

        # test we can read the file
        data = mock_data()
        with h5py.File(FILENAME, 'r') as file:
            load_logs(file, data)
        self.assertEqual(len(data.dict), 2)
        x, y = data.dict['Temp']
        self.assertArrays(x, np.asarray([1, 2], dtype=np.double))
        self.assertArrays(y, np.asarray([3, 4], dtype=np.double))

        x, y = data.dict['field']
        self.assertArrays(x, np.asarray([1.2, 2.2], dtype=np.double))
        self.assertArrays(y, np.asarray([6, 8], dtype=np.double))

        os.remove(FILENAME)

    @mock.patch('MuonDataLib.data.loader.'
                'load_events.Sample')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.EventsRawData')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.Source')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.User')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.EventsPeriods')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.Det1')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.MuonEventData')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.EventsCache')
    @mock.patch('MuonDataLib.data.loader.'
                'load_events.load_data')
    def test_load_events(self,
                         load_data,
                         cache,
                         muon_data,
                         detector_1,
                         periods,
                         user,
                         source,
                         raw_data,
                         sample):
        """
        Going to check that the function
        is called correctly by using mocks.
        The creation of the muon data
        object is covered by its own tests.
        """
        events = mock.Mock()
        load_data.return_value = (0, events)
        data_cache = mock.Mock()
        events.get_total_frames = mock.MagicMock(return_value=100)
        cache.return_value = data_cache
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'data_files',
                            'HIFI0.nxs')
        _ = load_events(file, 64)

        # check the read functions are called
        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()
        cache.assert_called_once()
        load_data.assert_called_once()
        # check muon data gets the correct read functions
        muon_data.assert_called_once_with(events,
                                          data_cache,
                                          sample=sample(),
                                          raw_data=raw_data(),
                                          source=source(),
                                          user=user(),
                                          periods=periods(),
                                          detector1=detector_1())


if __name__ == '__main__':
    unittest.main()
