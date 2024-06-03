

class Frame(object):
    """
    A frame objects contains event data
    for a period of time for a single detector.
    Methods:
    - add events: adds events to the frame.
    - clear: delects all event information from frame.

    Properties:
    - get_period: gets the period for the frame.
    - get_start_time: gets the start time for the frame.
    - get_event_times: gets the time stamps for the events.
    - get_event_amplitudes: gets the amplitudes for the events.
    """
    def __init__(self, start_time: float, period: int):
        """
        Creates an instance of a frame object.
        :param start_time: is the time (float) since the start of run.
        :param period: the period number for the frame.
        """
        self._start = start_time
        self._period = period

        self._event_times = []
        self._event_amplitudes = []

    def add_events(self, times, amps):
        """
        Adds events to the frame
        :param times: the time stamps for the events.
        :param amps: the amplitudes for the events.
        """
        self._event_times = times
        self._event_amplitudes = amps

    def clear(self):
        """
        Clears all data from the frame.
        """
        self._event_times = []
        self._event_amplitudes = []

    @property
    def get_period(self):
        """
        :returns: the period of the frame.
        """
        return self._period

    @property
    def get_start_time(self):
        """
        :returns: the start time of the frame.
        """
        return self._start

    @property
    def get_event_times(self):
        """
        :returns: the time stamps of the events
        """
        return self._event_times

    @property
    def get_event_amplitudes(self):
        """
        :returns: the event's amplitudes.
        """
        return self._event_amplitudes
