from MuonDataLib.data.events.detector import Detector
from MuonDataLib.test_helpers.unit_test import TestHelper
import unittest


class DetectorTest(TestHelper):

    def test_init(self):
        det = Detector(5)

        self.assertEqual(det._ID, 5)
        self.assertEqual(det._frames, {})
        self.assertEqual(det._current, -1)

    def test_add_new_frame(self):
        det = Detector(4)

        self.assertEqual(det._frames, {})

        det.add_new_frame(1.2, 0)
        self.assertEqual(len(det._frames), 1)
        self.assertEqual(list(det._frames.keys())[0], 0)
        self.assertEqual(det._current, 0)

        frame = det._frames[0]
        self.assertAlmostEqual(frame._start, 1.2)
        self.assertEqual(frame._period, 0)
        self.assertEqual(frame._event_times, [])
        self.assertEqual(frame._event_amplitudes, [])

    def test_add_events_to_frame(self):
        det = Detector(4)
        det.add_new_frame(1.2, 0)

        det.add_events_to_frame(0, [1, 2, 3], [3, 2, 1])

        frame = det._frames[0]
        self.assertAlmostEqual(frame._start, 1.2)
        self.assertEqual(frame._period, 0)
        self.assertArrays(frame._event_times, [1, 2, 3])
        self.assertArrays(frame._event_amplitudes, [3, 2, 1])

    def test_two_add_events_to_frame(self):
        det = Detector(4)
        det.add_new_frame(1.2, 0)
        det.add_events_to_frame(0, [1, 2, 3], [3, 2, 1])
        frame = det._frames[0]
        self.assertArrays(frame._event_times, [1, 2, 3])
        self.assertArrays(frame._event_amplitudes, [3, 2, 1])

        det.add_events_to_frame(0, [1, 2, 3, 4, 5, 6], [3, 2, 1, 6, 5, 4])
        frame = det._frames[0]
        self.assertArrays(frame._event_times, [1, 2, 3, 4, 5, 6])
        self.assertArrays(frame._event_amplitudes, [3, 2, 1, 6, 5, 4])

    def test_get_histogram(self):
        det = Detector(0)
        det.add_new_frame(0, 0)
        det.add_events_to_frame(0,
                                [1, 1.2, 2.3, 2.4, 5.],
                                [3, 2, 1, 1, 2])
        bin_edges = [0, 1, 2, 3, 4, 5, 6]
        hist, bins = det.get_histogram(bin_edges)
        self.assertArrays(bin_edges, bins)
        self.assertArrays(hist, [0, 2, 2, 0, 0, 1])

    def test_get_histogram_conversion(self):
        det = Detector(0)
        det.add_new_frame(0, 0)
        det.add_events_to_frame(0,
                                [1, 1.2, 2.3, 2.4, 5.],
                                [3, 2, 1, 1, 2])
        bin_edges = [0, 1, 2, 3, 4, 5, 6]
        hist, bins = det.get_histogram(bin_edges, 0.5)
        self.assertArrays(bin_edges, bins)
        self.assertArrays(hist, [2, 2, 1, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
