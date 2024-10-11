import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()



def sort_numpy(double[:] a, kind):
    np.asarray(a).sort(kind=kind)

def test_sort(a):
    start = time.time()
    _ = sort_numpy(a, 'quicksort')
    print('quick', time.time() - start)
   
    start = time.time()
    _ = sort_numpy(a, 'mergesort')
    print('merge', time.time() - start)

    start = time.time()
    _ = sort_numpy(a, 'heapsort')
    print('heap', time.time() - start)

    start = time.time()
    _ = sort_numpy(a, 'stable')
    print('stable', time.time() - start)



cpdef test(double[:] f_start, double[:] f_end, double dt):
    return [1], [2]

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
    cdef int N = len(j_start)
    cdef cnp.ndarray[int, ndim=1] _final_start = np.zeros(N, dtype=np.int32)
    cdef cnp.ndarray[int, ndim=1] _final_end = np.zeros(N, dtype=np.int32)
    cdef int[:] final_start = _final_start
    cdef int[:] final_end = _final_end

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
    return _final_start[:N], _final_end[:N]

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

import time
import numpy as np
from MuonDataLib.cython_ext.stats import make_histogram

cpdef do_stuff(int[:] IDs, double[:] times, int[:] start_j, double[:] start_t, double[:] f_start, double[:] f_end):

    mean = np.mean(np.asarray(start_t[1:]) - np.asarray(start_t[:-1]))
    start = time.time()
    a, b = get_indicies(f_start, f_end, mean)
    a, b = rm_overlaps(a, b)
    new_IDs = good_values_ints(a,b, start_j, IDs)
    new_times = good_values_double(a, b, start_j, times)
    f_time = time.time() - start
    start = time.time()
    _, _ = make_histogram(new_times, new_IDs, 960, 0, 32.768, 0.016)
    h_time = time.time() - start
    return f_time, h_time, f_time+h_time
