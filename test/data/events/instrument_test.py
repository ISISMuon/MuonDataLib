from MuonDataLib.data.events.instrument import Instrument, filter_data
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.utils import extract_event_data
import unittest
import numpy as np


DATE = '2024-05-23T09:03:23.85'


class InstrumentTest(TestHelper):

    def test_filter_data(self):
        data_0 = np.asarray([0, 1, 2, 3, 4, 5])
        data_1 = np.asarray([5, 4, 3, 2, 1, 0])

        filter_0, filter_1 = filter_data([data_0, data_1], data_0 > 2)
        self.assertArrays(filter_0, [3, 4, 5])
        self.assertArrays(filter_1, [2, 1, 0])

    def test_init(self):
        inst = Instrument(DATE, 2)
        self.assertEqual(inst._start, DATE)
        self.assertEqual(inst._current_frame, -1)
        self.assertEqual(inst._current_index, None)
        self.assertEqual(len(inst._detectors), 2)
        self.assertArrays(inst._bin_edges, np.arange(0, 30.5, .5))
        self.assertArrays(inst._bounds, [0, 30])
        self.assertEqual(inst._unit_conversion, 1e-3)

    def test_add_new_frame(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(0.1, 0, 0)
        self.assertEqual(inst._start, DATE)
        self.assertEqual(inst._current_frame, 0)
        self.assertEqual(inst._current_index, 0)

    def assertEvents(self, inst, ID, frame, times, amps, period, start):
        frame = extract_event_data(inst, ID, frame)
        self.assertArrays(frame.get_event_times, times)
        self.assertArrays(frame.get_event_amplitudes, amps)
        self.assertEqual(frame.get_period, period)
        self.assertEqual(frame.get_start_time, start)

    def test_add_data(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(0.1, 0, 0)
        inst._add_data(0,
                       [0, 1, 0, 1],
                       [1, 2, 3, 4],
                       [4, 3, 2, 1])
        self.assertEvents(inst, 0, 0,
                          [1, 3],
                          [4, 2],
                          0, 0.1)

    def test_add_event_data(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(1.2, 0, 0)

        inst.add_event_data([0, 1, 0, 1, 0, 1, 0],
                            [1, 2, 3, 4, 5, 6, 7],
                            [1, 2, 1, 2, 1, 2, 1],
                            [0, 0, 0, 0, 0, 0, 0],
                            [1.2], [0])

        self.assertEvents(inst, 0, 0,
                          [1, 3, 5, 7],
                          [1, 1, 1, 1],
                          0, 1.2)

        self.assertEvents(inst, 1, 0,
                          [2, 4, 6],
                          [2, 2, 2],
                          0, 1.2)

    def test_extend_current_frame(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(1.2, 0, 0)

        # just provide some data
        inst.add_event_data([0, 1, 0],
                            [1, 2, 3],
                            [1, 2, 1],
                            [0, 0, 0],
                            [1.2], [0])

        self.assertEvents(inst, 0, 0,
                          [1, 3],
                          [1, 1],
                          0, 1.2)

        self.assertEvents(inst, 1, 0,
                          [2],
                          [2],
                          0, 1.2)

        # update with more data
        inst.add_event_data([0, 1, 0, 1, 0, 1, 0],
                            [1, 2, 3, 4, 5, 6, 7],
                            [1, 2, 1, 2, 1, 2, 1],
                            [0, 0, 0, 0, 0, 0, 0],
                            [1.2], [0])

        self.assertEvents(inst, 0, 0,
                          [1, 3, 5, 7],
                          [1, 1, 1, 1],
                          0, 1.2)

        self.assertEvents(inst, 1, 0,
                          [2, 4, 6],
                          [2, 2, 2],
                          0, 1.2)

    def test_add_2_frames(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(1.2, 0, 0)

        inst.add_event_data([0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 2, 3, 4, 5, 6, 7, 8],
                            [1, 2, 1, 2, 2, 1, 2, 1],
                            [0, 0],
                            [1.2, 4.1],
                            [0, 4])

        self.assertEvents(inst, 0, 0,
                          [1, 3],
                          [1, 1],
                          0, 1.2)

        self.assertEvents(inst, 1, 0,
                          [2, 4],
                          [2, 2],
                          0, 1.2)

        # check frame 2
        self.assertEvents(inst, 0, 1,
                          [5, 7],
                          [2, 2],
                          0, 4.1)

        self.assertEvents(inst, 1, 1,
                          [6, 8],
                          [1, 1],
                          0, 4.1)

    def test_add_3_frames(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(1.2, 0, 0)

        inst.add_event_data([0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            [1, 2, 1, 2, 2, 1, 2, 1, 3, 4],
                            [0, 0, 0],
                            [1.2, 4.1, 8.6],
                            [0, 4, 8])

        self.assertEvents(inst, 0, 0,
                          [1, 3],
                          [1, 1],
                          0, 1.2)

        self.assertEvents(inst, 1, 0,
                          [2, 4],
                          [2, 2],
                          0, 1.2)

        # check frame 2
        self.assertEvents(inst, 0, 1,
                          [5, 7],
                          [2, 2],
                          0, 4.1)

        self.assertEvents(inst, 1, 1,
                          [6, 8],
                          [1, 1],
                          0, 4.1)
        # check frame 3
        self.assertEvents(inst, 0, 2,
                          [9],
                          [3],
                          0, 8.6)

        self.assertEvents(inst, 1, 2,
                          [10],
                          [4],
                          0, 8.6)

    def test_set_bins(self):
        inst = Instrument(DATE, 2)
        # change the bounds to make test simpiler
        inst._bounds = [1, 4]
        inst.set_bin_width(0.5)
        self.assertArrays(inst._bin_edges,
                          [1., 1.5, 2, 2.5, 3, 3.5, 4])

    def test_get_histogram(self):
        inst = Instrument(DATE, 2)
        inst.add_new_frame(1.2, 0, 0)

        inst.add_event_data([0, 1, 0, 1, 0, 1, 0, 1],
                            np.asarray([1, 2, 3, 4, 5, 6, 7, 8])*1.e3,
                            [1, 2, 1, 2, 2, 1, 2, 1],
                            [0, 0],
                            [1.2, 4.1],
                            [0, 4])
        inst._bounds = [0, 10]
        inst.set_bin_width(1.)
        # check detector 0
        y, x = inst.get_histogram(0)
        self.assertArrays(x, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertArrays(y, [0, 1, 0, 1, 0, 1, 0, 1, 0, 0])

        # check detector 1
        y, x = inst.get_histogram(1)
        self.assertArrays(x, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertArrays(y, [0, 0, 1, 0, 1, 0, 1, 0, 1, 0])


if __name__ == '__main__':
    unittest.main()
