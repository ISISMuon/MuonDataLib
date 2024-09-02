import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()


cdef class Fil:
    cdef double[:] data
    cdef double value
    cdef int status

    def __init__(self, data, value, status):
        self.data = data
        self.value = value
        self.status = status

    def set(self, int status, double value):
        self.value = value
        self.status = status

    def get_data(self):
        return self.data

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef make_histogram2(
        double[:] times,
        cnp.int32_t[:] spec,
        int N_spec,
        Fil fil,
        double min_time=0,
        double max_time=30.,
        double width=0.5,
        double conversion=1.e-3):
    """
    This method creates histograms from a list of data.
    It produces a matrix of histograms for multiple spectra.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :param conversion: for unit conversions
    :returns: a matrix of histograms, the bin edges
    """

    cdef Py_ssize_t det, k, j_bin
    cdef double time
    cdef int count = 0

    cdef cnp.ndarray[double, ndim=1] bins = np.arange(min_time, max_time + width, width, dtype=np.double)

    cdef cnp.ndarray[double, ndim=2] result = np.zeros((N_spec, len(bins)-1), dtype=np.double)
    cdef double[:, :] mat = result

    for k in range(len(times)):
        det = spec[k]
        time = times[k] * conversion
        if fil.status == 1 and fil.data[k] < fil.value:
            continue
        elif time <= max_time and time >= min_time:
            j_bin = int((time - min_time) // width)
            mat[det, j_bin] += 1. / width
            count += 1
    return result, bins, count


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef make_histogram(
        double[:] times,
        double[:] amps,
        double value,
        int status,
        cnp.int32_t[:] spec,
        int N_spec,
        double min_time=0,
        double max_time=30.,
        double width=0.5,
        double conversion=1.e-3):
    """
    This method creates histograms from a list of data.
    It produces a matrix of histograms for multiple spectra.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :param conversion: for unit conversions
    :returns: a matrix of histograms, the bin edges
    """

    cdef Py_ssize_t det, k, j_bin
    cdef double time

    cdef cnp.ndarray[double, ndim=1] bins = np.arange(min_time, max_time + width, width, dtype=np.double)

    cdef cnp.ndarray[double, ndim=2] result = np.zeros((N_spec, len(bins)-1), dtype=np.double)
    cdef double[:, :] mat = result

    for k in range(len(times)):
        det = spec[k]
        time = times[k] * conversion
        if status == 1 and amps[k] < value:
            continue
        elif time <= max_time and time >= min_time:
            j_bin = int((time - min_time) // width)
            mat[det, j_bin] += 1. / width
    return result, bins

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef make_histogram0(
        double[:] times,
        cnp.int32_t[:] spec,
        int N_spec,
        double min_time=0,
        double max_time=30.,
        double width=0.5,
        double conversion=1.e-3):
    """
    This method creates histograms from a list of data.
    It produces a matrix of histograms for multiple spectra.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :param conversion: for unit conversions
    :returns: a matrix of histograms, the bin edges
    """

    cdef Py_ssize_t det, k, j_bin
    cdef double time

    cdef cnp.ndarray[double, ndim=1] bins = np.arange(min_time, max_time + width, width, dtype=np.double)

    cdef cnp.ndarray[double, ndim=2] result = np.zeros((N_spec, len(bins)-1), dtype=np.double)
    cdef double[:, :] mat = result

    for k in range(len(times)):
        det = spec[k]
        time = times[k] * conversion

        if time <= max_time and time >= min_time:
            j_bin = int((time - min_time) // width)
            mat[det, j_bin] += 1. / width
    return result, bins

