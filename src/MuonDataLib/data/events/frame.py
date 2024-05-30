

class Frame(object):
    def __init__(self, start_time, period):
        """
        start_time is the time (float) since the start of run
        """
        self._start = start_time
        self._period = period

        self._event_times = []
        self._event_amplitudes = []

    def add_events(self, times, amps):
        self._event_times = times
        self._event_amplitudes = amps

    def clear(self):
        self._event_times = []
        self._event_amplitudes = []

    @property
    def get_period(self):
        return self._period

    @property
    def get_start_time(self):
        return self._start

    @property
    def get_event_times(self):
        return self._event_times

    @property
    def get_event_amplitudes(self):
        return self._event_amplitudes
