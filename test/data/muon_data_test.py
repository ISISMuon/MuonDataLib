from MuonDataLib.data.muon_data import MuonData, MuonEventData
import unittest
import os
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


class MuonEventDataTest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
