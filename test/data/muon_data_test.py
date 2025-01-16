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

    def test_MuonEventData_init(self):
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

        for key in data._dict.keys():
            self.assertEqual(key, data._dict[key])
        self.assertEqual(data._events, 'events')
        self.assertEqual(data._cache, 'cache')

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
        events.histogram = mock.Mock()

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
        events.histogram.assert_called_once_with(cache=cache)
        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()

        os.remove('tmp.nxs')

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
        events.histogram = mock.Mock()

        cache = mock.Mock()
        cache.empty = mock.Mock(return_value=False)

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

    def test_add_time_filter(self):
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

        data.add_time_filter('one', 0.03, 0.05)

        f_start, f_end = data._get_filters()
        self.assertEqual(len(f_start), 1)
        self.assertEqual(len(f_start), len(f_end))
        self.assertAlmostEqual(f_start['one'], 3e7)
        self.assertAlmostEqual(f_end['one'], 5e7)

    def test_remove_time_filter(self):
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

        data.add_time_filter('one', 0.03, 0.05)

        f_start, f_end = data._get_filters()
        self.assertEqual(len(f_start), 1)

        data.remove_time_filter('one')
        f_start, f_end = data._get_filters()
        self.assertEqual(len(f_start), 0)
        self.assertEqual(len(f_start), len(f_end))

    def test_report_filters(self):
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

        data.add_time_filter('one', 0.03, 0.05)
        data.add_time_filter('two', 0.01, 0.04)

        result = data.report_filters()

        keys = list(result.keys())
        self.assertEqual(len(keys), 2)
        self.assertArrays(result['one'], [0.03, 0.05])
        self.assertArrays(result['two'], [0.01, 0.04])

    def test_save_filters(self):
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

        data.add_time_filter('one', 0.03, 0.05)
        data.add_time_filter('two', 0.01, 0.04)

        data.save_filters('event_save.json')

        with open('event_save.json') as file:
            result = json.load(file)
        keys = list(result.keys())
        self.assertEqual(len(keys), 2)
        self.assertArrays(result['one'], [3e7, 5e7])
        self.assertArrays(result['two'], [1e7, 4e7])

        os.remove('event_save.json')

    def test_load_filters(self):
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

        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            'data_files',
                            'load_filter.json')

        data.load_filters(file)

        f_start, f_end = data._events._get_filters()
        keys = list(f_start.keys())
        self.assertEqual(keys[0], 'test')
        self.assertEqual(keys[1], 'unit')
        self.assertEqual(len(keys), 2)

        self.assertEqual(f_start['test'], 1.1)
        self.assertEqual(f_start['unit'], 3.1)
        self.assertEqual(f_end['test'], 8.2)
        self.assertEqual(f_end['unit'], 6.6)


if __name__ == '__main__':
    unittest.main()
