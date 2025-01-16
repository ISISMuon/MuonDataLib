from MuonDataLib.data.loader.load_events import load_events

import unittest
from unittest import mock
import os


class LoadEventsTest(unittest.TestCase):

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
