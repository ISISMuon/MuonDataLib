from MuonDataLib.data.events.frame import Frame
from MuonDataLib.test_helpers.nexus import NexusTestHelper
import unittest


class FrameTest(NexusTestHelper):

    def test_init(self):
        frame = Frame(4.2, 1)

        self.assertEqual(frame._start, 4.2)
        self.assertEqual(frame._period, 1)
        self.assertEqual(frame._event_times, [])
        self.assertEqual(frame._event_amplitudes, [])

    def test_add_events(self):
        frame = Frame(3.1, 2)
        frame.add_events([1, 2, 3], [3, 2, 1])
        self.assertArrays([1, 2, 3], frame._event_times)
        self.assertArrays([3, 2, 1], frame._event_amplitudes)

    def test_add_two_sets_of_events(self):
        frame = Frame(3.1, 2)
        frame.add_events([1, 2, 3], [3, 2, 1])
        self.assertArrays([1, 2, 3], frame._event_times)
        self.assertArrays([3, 2, 1], frame._event_amplitudes)
        # add the full array (should remove the already stored data)
        frame.add_events([1, 2, 3, 4, 5, 6], [3, 2, 1, 6, 5, 4])
        self.assertArrays([1, 2, 3, 4, 5, 6], frame._event_times)
        self.assertArrays([3, 2, 1, 6, 5, 4], frame._event_amplitudes)

    def test_clear(self):
        frame = Frame(3.1, 2)
        frame.add_events([1, 2, 3], [3, 2, 1])
        self.assertArrays([1, 2, 3], frame._event_times)
        self.assertArrays([3, 2, 1], frame._event_amplitudes)

        frame.clear()
        self.assertArrays([], frame._event_times)
        self.assertArrays([], frame._event_amplitudes)

    def test_get_period(self):
        frame = Frame(1.2, 1)
        self.assertEqual(frame.get_period, 1)

    def test_get_start_time(self):
        frame = Frame(0.1, 3)
        self.assertEqual(frame.get_start_time, 0.1)

    def test_get_events(self):
        frame = Frame(3.1, 2)
        frame.add_events([1, 2, 3], [3, 2, 1])
        self.assertArrays([1, 2, 3], frame.get_event_times)
        self.assertArrays([3, 2, 1], frame.get_event_amplitudes)


if __name__ == '__main__':
    unittest.main()
