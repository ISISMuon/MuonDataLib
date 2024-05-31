from MuonDataLib.data.loader.load_event import LoadEventData
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.utils import extract_event_data

import unittest
import os


class LoadEventDataTest(TestHelper):

    def assertEvents(self, inst, ID, frame, times, amps, period, start):
        frame = extract_event_data(inst, ID, frame)
        self.assertArrays(frame.get_event_times, times)
        self.assertArrays(frame.get_event_amplitudes, amps)
        self.assertEqual(frame.get_period, period)
        self.assertEqual(frame.get_start_time, start)

    def test_load_event_data(self):
        """
        """
        file = os.path.join(os.path.dirname(__file__),
                            '..',
                            '..',
                            'data_files',
                            'simple_test.nxs')
        load = LoadEventData()
        load.load_data(file)

        inst = load._inst

        self.assertEvents(inst, 0, 0,
                          [16, 602, 3846],
                          [10, 10, 10],
                          0,
                          0)

        self.assertEvents(inst, 60, 0,
                          [95, 836, 1055, 2734],
                          [10, 10, 10, 10],
                          0,
                          0)

        self.assertEvents(inst, 0, 1,
                          [127, 425, 491, 907, 957, 1207],
                          [10, 10, 10, 10, 10, 10],
                          0,
                          20000000)

    def test_reload_data(self):
        file_part = os.path.join(os.path.dirname(__file__),
                                 '..',
                                 '..',
                                 'data_files',
                                 'partial_run.nxs')
        file_full = os.path.join(os.path.dirname(__file__),
                                 '..',
                                 '..',
                                 'data_files',
                                 'complete_run.nxs')

        full_data = LoadEventData()
        full_data.load_data(file_full)

        load = LoadEventData()
        load.load_data(file_part)
        """
        since the file doesn't actually update
        we will manually change the file
        """
        load._file_name = file_full
        # check partial data is shorter
        self.assertLess(load._inst._current_frame,
                        full_data._inst._current_frame)

        load.reload_data()
        # check both end in the same state
        self.assertEqual(full_data._inst._start,
                         load._inst._start)

        self.assertEqual(full_data._inst._current_frame,
                         load._inst._current_frame)

        self.assertEqual(full_data._inst._current_index,
                         load._inst._current_index)

        for det in range(len(load._inst._detectors)):
            det_full = full_data._inst._detectors[det]
            det_part = load._inst._detectors[det]
            for frame in det_full._frames.keys():
                full_frame = det_full._frames[frame]
                part_frame = det_part._frames[frame]

                self.assertEqual(full_frame._start,
                                 part_frame._start)
                self.assertEqual(full_frame._period,
                                 part_frame._period)
                self.assertArrays(full_frame.get_event_times,
                                  part_frame.get_event_times)
                self.assertArrays(full_frame.get_event_amplitudes,
                                  part_frame.get_event_amplitudes)


if __name__ == '__main__':
    unittest.main()
