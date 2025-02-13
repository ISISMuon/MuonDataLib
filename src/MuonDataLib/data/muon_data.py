import h5py
from MuonDataLib.data.sample_logs import SampleLogs
from MuonDataLib.data.utils import NONE
import numpy as np
import json


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


ns_to_s = 1.e-9


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
        self._time_filter = {}
        self._keep_times = {}
        super().__init__(sample, raw_data, source, user, periods, detector1)
        self._dict['logs'] = SampleLogs()

    def _filter_logs(self):
        # if only resolution changed
        # -> filters are the same so can skip this

        # remove time filters
        for name in self._time_filter.keys():
            start, end = self._time_filter[name]
            self._events.add_filter(name, start/ns_to_s, end/ns_to_s)

        # keep time filters
        N = len(self._keep_times)
        if N > 0:
            data_end = self.get_frame_start_times()[-1] + 1.
            # remove from start (assume 0) to first window
            self._events.add_filter('keep_0', 0.0,
                                    self._keep_times[0][0]/ns_to_s)
            for j in range(1, len(self._keep_times)):
                self._events.add_filter(f'keep_{j}',
                                        self._keep_times[j-1][1]/ns_to_s,
                                        self._keep_times[j][0]/ns_to_s)
            self._events.add_filter(f'keep_{N}',
                                    self._keep_times[N-1][1]/ns_to_s,
                                    data_end/ns_to_s)

        log_names = self._dict['logs'].get_names()
        for name in log_names:
            result = self._dict['logs'].get_filter(name)
            self._events.apply_log_filter(*result)

        # apply the filters from the logs
        filters = self.report_filters().values()
        if not filters:
            return
        filter_times = list(filters)
        filter_times = np.asarray([np.asarray(filter_times[k],
                                              dtype=np.double)
                                   for k in range(len(filter_times))],
                                  dtype=np.double)
        self._dict['logs'].apply_filter(filter_times)

    def histogram(self, resolution=0.016):
        is_cache_empty = self._cache.empty()
        if is_cache_empty:
            self._filter_logs()
        if is_cache_empty or self._cache.get_resolution() != resolution:
            return self._events.histogram(width=resolution,
                                          cache=self._cache)
        return self._cache.get_histograms()

    def save_histograms(self, file_name, resolution=0.016):
        """
        Method for saving the object to a muon
        nexus v2 histogram file
        :param file_name: the name of the file to save to
        """
        self.histogram(resolution)
        super().save_histograms(file_name)

    def clear_filters(self):
        self._cache.clear()
        self._dict['logs'].clear_filters()
        self._time_filters.clear()
        self._events.clear_filters()

    def add_sample_log(self, name, x_data, y_data):
        self._cache.clear()
        self._dict['logs'].add_sample_log(name, x_data, y_data)

    def get_sample_log(self, name):
        return self._dict['logs'].get_sample_log(name)

    def keep_data_sample_log_below(self, log_name, max_value):
        self._dict['logs'].add_filter(log_name, NONE, max_value)

    def keep_data_sample_log_above(self, log_name, min_value):
        self._dict['logs'].add_filter(log_name, min_value, NONE)

    def keep_data_sample_log_between(self, log_name, min_value, max_value):
        if max_value <= min_value:
            raise RuntimeError("The max filter value is smaller "
                               "than the min value")
        self._dict['logs'].add_filter(log_name, min_value, max_value)

    def only_keep_data_time_between(self, times):
        # add check in order and correct format
        self._cache.clear()
        self._keep_times = times

    def delete_sample_log_filter(self, name):
        self._dict['logs'].clear_filter(name)

    def delete_only_keep_data_time_between(self):
        self._cache.clear()
        self._keep_times = []

    def remove_data_time_between(self, name, start, end):
        if name in self._time_filter.keys():
            raise RuntimeError(f'The name {name} already exists')
        self._cache.clear()
        self._time_filter[name] = (start, end)

    def delete_remove_data_time_between(self, name):
        self._cache.clear()
        del self._time_filter[name]

    def get_frame_start_times(self):
        """
        A method to get the frame start times
        :returns: the frame start times
        """
        return self._events.get_start_times()*ns_to_s

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
        self._cache.clear()
        self._events.add_filter(name, start/ns_to_s, end/ns_to_s)

    def remove_time_filter(self, name):
        """
        A method to remove a specific time filter.
        :param name: the name of the filter to remove
        """
        self._cache.clear()
        self._events.remove_filter(name)

    def clear_time_filters(self):
        """
        A method to clear all of the time filters
        """
        self._cache.clear()
        self._events.clear_filters()

    def _get_filters(self):
        """
        A method to get the filters for testing
        This will return the values in ns and not s.
        i.e. the native units for the event object
        :return the filter dicts
        """
        return self._events._get_filters()

    def report_filters(self):
        data = self._events.report_filters()
        for key in data.keys():
            data[key] = [x*ns_to_s for x in data[key]]
        return data

    def load_filters(self, file_name):
        """
        A method to filters from a json file.
        This will apply all of the filters from the file.
        :param file_name: the name of the json file
        """
        self._cache.clear()
        self._events.clear_filters()
        with open(file_name, 'r') as file:
            data = json.load(file)
        tmp = data['time_filters']
        self._time_filter = tmp['remove_filters']

        tmp = tmp['keep_filters']
        self._keep_times = []
        for val in tmp.values():
            self._keep_times.append(val)

        tmp = data['sample_log_filters']
        for name in tmp.keys():
            self._dict['logs'].add_filter(name, *tmp[name])

    def save_filters(self, file_name):
        """
        A method to save the current filters to a file.
        :param file_name: the name of the json file to save to.
        """
        data = {}
        tmp = {f'keep_{j}': self._keep_times[j]
               for j in range(len(self._keep_times))}
        data['time_filters'] = {'remove_filters': self._time_filter,
                                'keep_filters': tmp}
        tmp = {}
        for name in self._dict['logs'].get_names():
            result = self._dict['logs'].get_filter(name)
            if result[3] != NONE or result[4] != NONE:
                tmp[name] = [result[3], result[4]]
        data['sample_log_filters'] = tmp

        with open(file_name, 'w') as file:
            json.dump(data, file, ensure_ascii=False,
                      sort_keys=True, indent=4)
