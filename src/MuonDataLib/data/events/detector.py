from MuonDataLib.data.events.frame import Frame
import numpy as np


class Detector(object):
    """
    The Detector class represents a single
    detector for an instrument.
    A detector records events in frames.

    Methods:
    - add_new_frame
    - add_events_to_frame
    - get_histogram

    """
    def __init__(self, ID):
        """
        Creates a Detector
        :param ID: The identifier for
        the detector (e.g. detector number)
        """
        self._ID = ID
        self._frames = {}
        self._current = -1

    def add_new_frame(self, time, period):
        """
        Adds a new frame to the detector.
        :param time: the start time of
        the frame in ns.
        :param period: the period of the frame.
        """
        time_in_nsec = time
        self._current += 1
        self._frames[self._current] = Frame(time_in_nsec, period)

    def add_events_to_frame(self, frame, times, amps):
        """
        Adds events to a specific frame.
        :param frame: the frame number to add events to.
        :param time: the event time stamps to add
        :param amps: the event amplitudes to add
        """
        self._frames[frame].add_events(times, amps)

    def get_histogram(self, bin_edges, unit_conversion=1):
        """
        Generates a histogram for the detector.
        :param bin_edges: the bin edges to use in the histogram.
        :param unit_conversion: A conversion factor for units (e.g.
        ns to micro seconds).
        :returns: The histogram y values, bin edges.
        """
        events = np.asarray([])
        for frame in self._frames.keys():
            events = np.append(events, self._frames[frame].get_event_times)
        return np.histogram(events * unit_conversion,
                            bins=bin_edges)
