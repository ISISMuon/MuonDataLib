# cython: c_string_type=unicode, c_string_encoding=utf8

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector
import numpy as np
cimport numpy as cnp
cnp.import_array()


cdef extern from "_utils.h":
    vector[double] remove_from_vector(vector[double] vec, int index)

    cdef cppclass _MinFilter:
        _MinFilter() except +
        _MinFilter(vector[double] data) except +
        vector[double] data
        double _min
        bool active
        bool IsActive()
        void SetValue(double value)
        void Remove()
        bool Filter(int k)
        vector[double] GetData()

    cdef cppclass _FilterManager:
        _FilterManager() except +
        _FilterManager(vector[double] data) except +
        vector[double] times
        double _min2
        bool active2
        bool IsActive()
        _MinFilter min_filter
        void SetMinFilter(vector[double] input_data, double value)
        void Remove()
        vector[double] Filter()
        vector[double] GetData()

cdef class MF:
    cdef _MinFilter* thisptr

    def __cinit__(self, vector[double] &data):
        #cdef vector[double] *vec = data
        self.thisptr = new _MinFilter(data)

    def __dealloc__(self):
        del self.thisptr

    def is_active(self):
        return self.thisptr.IsActive()

    def set_value(self, value):
        self.thisptr.SetValue(value)

    def remove(self):
        self.thisptr.Remove()

    def filter(self, int k):
        return self.thisptr.Filter(k)

    def stats(self):
        data = self.thisptr.GetData()
        return (np.min(data),
                np.mean(data),
                np.max(data))

cdef class FM:
    cdef _FilterManager* thisptr

    def __cinit__(self, cnp.ndarray[double] data):
        self.thisptr = new _FilterManager(data)

    def __dealloc__(self):
        del self.thisptr

    def is_active(self):
        return self.thisptr.IsActive()

    def set_min_filter(self, data, value):
        self.thisptr.SetMinFilter(data, value)

    def remove(self):
        self.thisptr.Remove()

    def filter(self):
        return self.thisptr.Filter()

    def stats(self):
        data = self.thisptr.GetData()
        return (np.min(data),
                np.mean(data),
                np.max(data))

def erase_from_vector(vec, index):
    return remove_from_vector(vec, index)


