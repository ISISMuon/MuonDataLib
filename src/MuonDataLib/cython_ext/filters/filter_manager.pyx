from MuonDataLib.cython_ext.filters.frame_filter import FrameFilter
from MuonDataLib.cython_ext.filters.min_filter import MinFilter
import numpy as np
import json

class FilterManager(object):
    def __init__(self,
                 frames,
                 frame_times,
                 int N):

        self.frame_filter = FrameFilter(frames,
                                        frame_times,
                                        N)
        self.min_filters = {}

    def call(self, int k):
        # need to filter frames first
        for key in self.min_filters.keys():
            tmp = self.min_filters[key]
            # no need to carry on if any return false
            if tmp.is_active:
                return tmp.call(k)
        return 1

    def get_data(self, data):
        result = self.frame_filter.filter_data()
        inc = np.ones(len(data), dtype=int)
        if result == []:
            return inc

        for k in range(len(result) //2):
            # the plus 1 should be in the frame code...
            inc[result[2*k]:result[2*k+1]+1] = 0

        for key in self.min_filters.keys():
            inc = inc * self.min_filters[key].do()

        return inc



    def report(self):
        filters = {'frame filters': self.frame_filter.report()}
        tmp = {}
        for key in self.min_filters.keys():
            min_filter = self.min_filters[key]
            if min_filter.is_active:
                tmp[key] = min_filter.value()
        filters['min filters'] = tmp
        return filters

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.report(), f)

    def load(self, file_name):
        with open(file_name, 'r') as f:
            filters = json.load(f)
        tmp = filters['frame filters']
        for key in tmp.keys():
            self.add_frame_filter(key,
                                  tmp[key][0],
                                  tmp[key][1])

        tmp = filters['min filters']
        errors = []
        for key in tmp.keys():
            if key in self.min_filters.keys():
                self.set_min_filter(key, tmp[key])
            else:
                errors.append(key)
        if len(errors) > 0:
            msg = "The following keys were not recognised \n"
            for err in errors:
                msg += '  - ' + err + ' \n'
            raise ValueError(msg)


    """
    Min filter methods
    """
    def create_min_filter(self, str name, data):
        self.min_filters[name] = MinFilter(data)

    def _check_min_filter(self, str name):
        if name not in self.min_filters.keys():
            raise ValueError(f"{name} is not a recognised filter")

    def set_min_filter(self, str name, double min_value):
        self._check_min_filter(name)
        self.min_filters[name].set_min_filter(min_value)

    def remove_min_filter(self, str name):
        self._check_min_filter(name)
        self.min_filters[name].remove_min_filter(name)

    def get_stats(self, str name):
        return self.min_filters[name].get_stats()

    """
    frame filter methods
    """
    def frame_info(self):
        return self.frame_filter.frame_info()

    def add_frame_filter(self, str name, double start, double end):
        self.frame_filter.add_filter(name, start, end)

    def remove_frame_filter(self, str name):
        self.frame_filter.remove(name)

    def apply(self, data):
        return self.frame_filter.apply_filter(data)

    def get_good_frame_data(self, data):
        result = self.frame_filter.filter_data()
        inc = np.ones(len(data), dtype=int)
        if result == []:
            return inc
        for k in range(len(result) //2):
            # the plus 1 should be in the frame code...
            inc[result[2*k]:result[2*k+1]+1] = 0
        return inc

    def offset(self, data):
        result = self.frame_filter.filter_data()
        inc = np.zeros(len(data), dtype=np.double)
        if result == []:
            return inc
        for k in range(len(result) //2):
            # the plus 1 should be in the frame code...
            inc[result[2*k]:result[2*k+1]+1] = 10000.0
        return inc

