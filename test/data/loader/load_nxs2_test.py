from MuonDataLib.data.loader.load_nxs2 import load_nxs2

import unittest
from unittest import mock
import os


class LoadNxs2Test(unittest.TestCase):

    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.read_sample_from_histogram')
    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.read_raw_data_from_histogram')
    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.read_source_from_histogram')
    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.read_user_from_histogram')
    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.read_periods_from_histogram')
    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.read_detector1_from_histogram')
    @mock.patch('MuonDataLib.data.loader.'
                'load_nxs2.MuonData')
    def test_load_nxs2(self,
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
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'data_files',
                            'HIFI00180594.nxs')
        load_nxs2(file)

        # check the read functions are called
        sample.assert_called_once()
        raw_data.assert_called_once()
        source.assert_called_once()
        user.assert_called_once()
        periods.assert_called_once()
        detector_1.assert_called_once()

        # check muon data gets the correct read functions
        muon_data.assert_called_once_with(sample=sample(),
                                          raw_data=raw_data(),
                                          source=source(),
                                          user=user(),
                                          periods=periods(),
                                          detector1=detector_1())


if __name__ == '__main__':
    unittest.main()
