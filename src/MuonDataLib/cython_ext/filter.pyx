import numpy as np
cimport numpy as cnp
import cython
import json
cnp.import_array()


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef get_indicies(double[:] f_start, double[:] f_end, double dt):
    cdef int N = len(f_start)
    cdef cnp.ndarray[int, ndim=1] _j_start = np.zeros(N, dtype=np.int32)
    cdef cnp.ndarray[int, ndim=1] _j_end = np.zeros(N, dtype=np.int32)
    cdef int j
    cdef int[:] j_start = _j_start
    cdef int[:] j_end = _j_end

    for j in range(N):
        j_start[j] = int(f_start[j]/dt)
        j_end[j] = int(f_end[j]/dt)

    return _j_start, _j_end

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef rm_overlaps(int[:] j_start, int[:] j_end):
    """
    Assume that the start and end frame values are in order.
    """
    cdef int N = len(j_start)
    cdef cnp.ndarray[int, ndim=1] _final_start = np.zeros(N, dtype=np.int32)
    cdef cnp.ndarray[int, ndim=1] _final_end = np.zeros(N, dtype=np.int32)
    cdef int[:] final_start = _final_start
    cdef int[:] final_end = _final_end

    cdef int one = 1
    cdef int start = j_start[0]
    cdef int end = j_end[0]
    cdef int k, next_start, next_end

    N = 0
    for k in range(1, len(j_start)):
        next_start = j_start[k]
        next_end = j_end[k]

        # no overlap
        if end < next_start:
            final_start[N] = start
            final_end[N] = end
            N += 1
            start = next_start
            end = next_end

        # overlap
        elif next_end > end:
            end = next_end

    final_start[N] = start
    final_end[N] = end
    N = N+1
    return _final_start[:N], _final_end[:N], np.sum(one + _final_end[:N] - _final_start[:N])


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef good_values_ints(int[:] f_start, int[:] f_end, int[:] start_index, int[:] IDs):
    cdef Py_ssize_t start = 0
    cdef cnp.ndarray[int] _good_IDs = np.zeros(len(IDs), dtype=np.int32)
    cdef int[:] good_IDs = _good_IDs
    cdef Py_ssize_t k, last
    cdef Py_ssize_t v, N
    cdef Py_ssize_t M = len(f_start)
    N = 0

    for k in range(M):
        last = start_index[f_start[k]]
        for v in range(start, last):
            good_IDs[N] = IDs[v]
            N += 1
        start = start_index[f_end[k] + 1]

    # check if filter covers last frame
    if f_end[M-1] + 1 >= len(start_index):
        return _good_IDs[:N]
    last = len(IDs)
    for v in range(start, last):
        good_IDs[N] = IDs[v]
        N += 1
    return _good_IDs[:N]

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef good_values_double(int[:] f_start, int[:] f_end, int[:] start_index, double[:] IDs):
    cdef Py_ssize_t start = 0
    cdef cnp.ndarray[double] _good_IDs = np.zeros(len(IDs), dtype=np.double)
    cdef double[:] good_IDs = _good_IDs
    cdef Py_ssize_t k, last
    cdef Py_ssize_t v, N
    cdef Py_ssize_t M = len(f_start)
    N = 0

    for k in range(M):
        last = start_index[f_start[k]]
        for v in range(start, last):
            good_IDs[N] = IDs[v]
            N += 1
        start = start_index[f_end[k] + 1]

    # check if filter covers last frame
    if f_end[M-1] + 1 >= len(start_index):
        return _good_IDs[:N]
    last = len(IDs)
    for v in range(start, last):
        good_IDs[N] = IDs[v]
        N += 1
    return _good_IDs[:N]

def save_filters(file, start_times, end_times):
    data = {}
    for key in start_times.keys():
        data[key] = (start_times[key], end_times[key])
    json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=4)

def read_filters(file):
    data = json.load(file)
    return data
