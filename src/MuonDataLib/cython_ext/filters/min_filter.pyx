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


cdef class MinFilter:
    cdef readonly double[:] data
    cdef readonly double min_value
    cdef readonly bool active

    def __init__(self, data):
        self.data = data
        self.min_value = 0.
        self.active = False

    def set_min_filter(self, double min_value):
        self.min_value = min_value
        self.active = True

    def remove_min_filter(self):
        self.active = False

    def get_stats(self):
        return (np.min(self.data),
                np.mean(self.data),
                np.median(self.data),
                np.max(self.data))

    def value(self):
        return self.min_value

    @property
    def is_active(self):
        return self.active

    def __call__(self, int k):
        return self.data[k] < self.min_value

