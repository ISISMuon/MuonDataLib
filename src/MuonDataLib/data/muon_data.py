import h5py


class MuonData(object):
    """
    A class to store all of the information needed for muon data
    """
    def __init__(self, sample, raw_data, source, user, periods, detector1):
        """
        Creates a store for relevant muon data (defined by nxs v2)
        :param sample: the Sample data needed for nexus v2 file
        :param raw_data: the RawData data needed for nexus v2 file
        :param source: the Source data needed for nexus v2 file
        :param user: the User data needed for nexus v2 file
        :param periods: the Periods data needed for nexus v2 file
        :param detector1: the Detector1 data needed for nexus v2 file
        """
        self._dict = {}
        self._dict['raw_data'] = raw_data
        self._dict['sample'] = sample
        self._dict['source'] = source
        self._dict['user'] = user
        self._dict['periods'] = periods
        self._dict['detector_1'] = detector1

    def save_histograms(self, file_name):
        """
        Method for saving the object to a muon
        nexus v2 histogram file
        :param file_name: the name of the file to save to
        """
        file = h5py.File(file_name, 'w')
        for key in self._dict.keys():
            self._dict[key].save_nxs2(file)
        file.close()
        return


class MuonEventData(MuonData):
    def __init__(self, events, cache, sample, raw_data, source, user,
                 periods, detector1):
        """
        Creates a store for relevant muon data (defined by nxs v2)
        :param events: the event data
        :param cache: the cache for the event data
        :param sample: the Sample data needed for nexus v2 file
        :param raw_data: the RawData data needed for nexus v2 file
        :param source: the Source data needed for nexus v2 file
        :param user: the User data needed for nexus v2 file
        :param periods: the Periods data needed for nexus v2 file
        :param detector1: the Detector1 data needed for nexus v2 file
        """
        self._events = events
        self._cache = cache
        super().__init__(sample, raw_data, source, user, periods, detector1)

    def save_histograms(self, file_name):
        """
        Method for saving the object to a muon
        nexus v2 histogram file
        :param file_name: the name of the file to save to
        """
        if self._cache.empty():
            self._events.histogram(cache=self._cache)
        super().save_histograms(file_name)

    def get_frame_start_times(self):
        """
        A method to get the frame start times
        :returns: the frame start times
        """
        return self._events.get_start_times()

    def add_time_filter(self, name, start, end):
        """
        A method to add time based filters.
        The inputs to this are in seconds relative
        to the start of the run. The events object
        takes time in ns.
        The filter will include the whole frame
        when a time is part way into a frame.
        :param name: the name of the filter
        :param start: the start time for the filter
        :param end: the end time for the filter
        """
        self._events.add_filter(name, start*1.e-9, end*1.e-9)

    def remove_time_filter(self, name):
        """
        A method to remove a specific time filter.
        :param name: the name of the filter to remove
        """
        self._events.remove_filter(name)

    def clear_time_filters(self):
        """
        A method to clear all of the time filters
        """
        self._events.clear_filters()
