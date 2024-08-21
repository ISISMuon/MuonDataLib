import numpy as np
cimport numpy as cnp
import cython
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.algorithm cimport sort as sort
cnp.import_array()


cdef vector[double] my_sort(vector[double] times):
    """
    A simple wrapper for a vector sort
    :param times: the times of the data to be sorted
    :return: a sorted list of time
    """
    sort(times.begin(), times.end())
    return times


cdef class MaxFilter:
    cdef readonly double[:] data
    cdef readonly double max_value
    cdef readonly bool active

    def __init__(self,
                 cnp.ndarray[double] data):
        self.data = data
        self.max_value = 0.
        self.active = False

    def set_min_filter(self, double min_value):
        self.min_value = min_value
        self.active = True

    def remove_min_filter(self):
        self.active = False

    @property
    def is_active(self):
        return self.active

    def __call__(self, int k):
        return self.data[k] < self.min_value


class MinFilterManager(object):
    def __init__(self):
        self.filters = {}

    def create_min_filter(self, name, data):
        self.filters[name] = MinFilter(data)

    def set_min_filter(self, name, min_value):
        self.filters[name].set_min_filter(min_value)

    def __call__(self, k):
        for key in self.filters.keys():
            # no need to carry on if any return false
            if self.filters[key].is_active and self.filters[key](k):
                return False
        return True
