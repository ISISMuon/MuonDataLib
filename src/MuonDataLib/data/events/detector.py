from MuonDataLib.data.events.frame import Frame
import numpy as np


class Detector(object):
    def __init__(self, ID):
        self._ID = ID
        self._frames = {}
        self._current = -1

    def add_new_frame(self, time, period):
        """
        time is in ns
        """
        time_in_nsec = time
        self._current += 1
        self._frames[self._current] = Frame(time_in_nsec, period)

    def add_events_to_frame(self, frame, times, amps):
        self._frames[frame].add_events(times, amps)

    def get_histogram(self, bin_edges, unit_conversion=1):
        events = np.asarray([])
        for frame in self._frames.keys():
            events = np.append(events, self._frames[frame].get_event_times)
        return np.histogram(events * unit_conversion,
                            bins=bin_edges)
