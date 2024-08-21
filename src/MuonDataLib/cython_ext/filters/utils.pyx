# cython: c_string_type=unicode, c_string_encoding=utf8

from libcpp.vector cimport vector

cdef extern from "_utils.h":
    vector[double] remove_from_vector(vector[double] vec, int index)

def erase_from_vector(vec, index):
    return remove_from_vector(vec, index)
