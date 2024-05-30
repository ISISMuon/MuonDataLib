from MuonDataLib.data.events.frame import Frame


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
