from MuonDataLib.data.utils import NONE
from MuonDataLib.cython_ext.utils import binary_search
import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef get_indices(double[:] times, double[:] f_start, double[:] f_end,
                  str name='value', str unit=''):
    """
    Method for calculating which frames filters belong to.
    This assumes that all data is in order.
    It uses a binary search to find the index of the left bound of the bin
    containing the desired value. Since the filter times are in order
    the next search can have a start value of equal to the index found for
    the previous filter. Similarly the first end filter must be after the
    start for the first filter.


    :param times: the list of frame start times
    :param f_start: a list of filter start times
    :param f_end: a list of filter end times
    :param name: the name of the thing we are filtering on
    :param unit: the unit of the thing being filtered
    :result: the list of start and end frame indices for the filters
    """
    cdef int N = len(f_start)
    cdef int M = len(times)
    cdef cnp.ndarray[int, ndim=1] _j_start = np.zeros(N, dtype=np.int32)
    cdef cnp.ndarray[int, ndim=1] _j_end = np.zeros(N, dtype=np.int32)
    cdef int j
    cdef int[:] j_start = _j_start
    cdef int[:] j_end = _j_end

    cdef int start = 0

    for j in range(N):
        j_start[j] = binary_search(times, start, M, f_start[j], name, unit)
        start = j_start[j]

    # the first end filter must be after the first start filter
    start = j_start[0]
    for j in range(N):
        j_end[j] = binary_search(times, start, M, f_end[j], name, unit)

    return _j_start, _j_end

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef rm_overlaps(int[:] j_start, int[:] j_end, int[:] periods):
    """
    Assume that the start and end frame values are in order.
    They can overlap, this code will remove the overlaps.

    Let o be filter 1, x be filter 2, | is a frame boundary

    The original unfiltered data:

    |    |    |    |    |    |    |    |    |    |

    with filter one

    |o o |    |    |    |   o|    |  o |    |    |

    with filter two

    |o o | x  | x  |    |   o| x  |  o | x  |    |

    Then this code will return filters for (added
    frame numbers to make it easier)

    1    2    3    4    5    6    7    8    9    10
    |o o | x  | x  |    |   o| x  |  o | x  |    |

    frame 1 to 1
    frame 2 to 3
    frame 5 to 8

    Notice that this includes an overlap between the two filters,
    but the inner bounds have been removed.

    :param j_start: the start indices for the filtered frames
    :param j_end: the end indices for the filtered frames
    :return: the list of start and end indices for the filtered
    frames (excluding internal overlaps between filters) and the
    number of removed frames.
    """
    # there will be at most the same number of filters
    cdef int N = len(j_start)
    cdef cnp.ndarray[int, ndim=1] _final_start = np.zeros(N, dtype=np.int32)
    cdef cnp.ndarray[int, ndim=1] _final_end = np.zeros(N, dtype=np.int32)
    cdef int[:] final_start = _final_start
    cdef int[:] final_end = _final_end
    cdef int one = 1
    cdef int start = j_start[0]
    cdef int end = j_end[0]
    cdef int k, next_start, next_end, j

    # due to overlaps the number of filters might be smaller
    N = 0
    for k in range(1, len(j_start)):
        next_start = j_start[k]
        next_end = j_end[k]

        # no overlap in filters
        if end < next_start:
            final_start[N] = start
            final_end[N] = end
            N += 1
            start = next_start
            end = next_end

        # overlap in filters
        elif next_end > end:
            end = next_end

    # get the last set of filters
    final_start[N] = start
    final_end[N] = end
    N = N+1

    # get removed frames
    cdef int[:] rm_frames = np.zeros(np.max(periods) + 1, dtype=np.int32)
    for k in range(N):
        start = _final_start[k]
        for j in range(_final_end[k] - start + 1):
            rm_frames[periods[start + j]] += 1

    return _final_start[:N], _final_end[:N], rm_frames


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef good_periods(int[:] f_start, int[:] f_end, int[:] start_index, int[:] periods, int N_events):
    """
    This removes the values from the array corresponding to the filtered frames.
    :param f_start: the start indices for the filters (no overlaps)
    :param f_end: the end indices for the filters (no overlaps)
    :param start_index: a list that gives the first index in int_array for that frame
    :param periods: the array identifing the period for each frame
    :param N_events: the number of events
    :return: An array of the periods for each event
    """

    cdef Py_ssize_t start = 0
    cdef Py_ssize_t k, M, j, end, dm, filter_start
    cdef Py_ssize_t len_filters = len(f_start)
    cdef Py_ssize_t N_frames = len(start_index)
    cdef cnp.ndarray[int] _good_periods = np.zeros(N_events,
                                                   dtype=np.int32)
    cdef int[:] good_periods = _good_periods
    start = 0
    M = 0
    j = 0
    if len_filters > 0:
        filter_start = f_start[0]
    else:
        filter_start = N_events + 1

    for k in range(N_frames - 1):
        if k < filter_start:
            end = start_index[k+1]
            dm = end - start
            good_periods[M:M+dm] = periods[k]
            M += dm
            start = end
        elif k == f_end[j]:
            j += 1
            start = start_index[k+1]
            if j == len_filters:
                filter_start = N_events + 1
            else:
                filter_start = f_start[j]

    dm = N_events - start_index[N_frames-1]
    good_periods[M:M + dm] = periods[len(periods)-1]
    M += dm
    return _good_periods[:M]

ctypedef fused int_double:
    double
    int

cpdef good_values_ints(int[:] f_start, int[:] f_end, int[:] start_index,
                          int[:] array):
    cdef int[:] start_, end_, delta
    cdef int N

    start_, end_, delta, N = _get_good_frames(f_start, f_end, start_index, array)
    
    cdef cnp.ndarray[int] good_array = np.zeros(N, dtype=np.int32)
    cdef int[:] _good_array = good_array
    return _apply_good_frames(start_, end_, start_index, array, delta, _good_array)

cpdef good_values_double(int[:] f_start, int[:] f_end, int[:] start_index,
                          double[:] array):
    cdef int[:] start_, end_, delta
    cdef int N

    start_, end_, delta, N = _get_good_frames(f_start, f_end, start_index, array)
    cdef cnp.ndarray[double] good_array = np.zeros(N, dtype=np.double)
    cdef double[:] _good_array = good_array
    return _apply_good_frames(start_, end_, start_index, array, delta, _good_array)

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef _get_good_frames(int[:] f_start, int[:] f_end, int[:] start_index, int_double[:] array):
    """
    This removes the values from the array corresponding to the filtered frames.
    :param f_start: the start indices for the filters (no overlaps)
    :param f_end: the end indices for the filters (no overlaps)
    :param start_index: a list that gives the first index in int_array for that frame
    :param int_array: the array to remove data from
    :return: the int_array with the data in the filtered frames removed
    """

    cdef int start = 0

    cdef cnp.ndarray[int] start_ = np.zeros(len(f_start), dtype=np.int32)
    cdef cnp.ndarray[int] end_ = np.zeros(len(f_start), dtype=np.int32)
    cdef Py_ssize_t k
    cdef Py_ssize_t z = 0
    cdef int M = len(f_start) - 1

    for k in range(len(f_start)-1):
        start_[k] = start_index[f_start[k]]
        end_[k] = start_index[f_end[k] + 1]
    start_[M] = start_index[f_start[M]]

    if len(start_index) == f_end[M] + 1:
        end_[M] = len(array)
    else:
        end_[M] = start_index[f_end[M] + 1]

    cdef int[:] delta = end_ - start_
    cdef int N = len(array) - np.sum(delta)

    return start_, end_, delta, N

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef _apply_good_frames(int[:] start_, int[:] end_, int[:] start_index,
                         int_double[:] array,
                         int[:] delta,
                         int_double[:] good_array):
    """
    This removes the values from the array corresponding to the filtered frames.
    :param f_start: the start indices for the filters (no overlaps)
    :param f_end: the end indices for the filters (no overlaps)
    :param start_index: a list that gives the first index in int_array for that frame
    :param int_array: the array to remove data from
    :return: the int_array with the data in the filtered frames removed
    """
    cdef int a, b, c
    cdef Py_ssize_t k, f
    cdef int z = 0

    if start_[z] > start_index[z]:
        a = start_[z]
        good_array[z:a] = array[z:a]

    for k in range(1, len(start_)):

        a = end_[k-1]
        b = start_[k]
        c = np.sum([delta[f] for f in range(k)])
        good_array[a - c: a -c + b -a ] = array[a:b]

    if int_double is int:
        return np.asarray(good_array, dtype=np.int32)
    else:
        return np.asarray(good_array, dtype=np.double)


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef apply_filter(x, y, times):
    """
    Applies the time filters to the sample log values
    :param x: the x values for the sample log
    :param y: the y values for the sample log
    :param times: a list of the [start, end] times
    within which the data will be removed
    """
    fx = np.zeros(len(x))
    fy = np.zeros(len(y))
    # need to make sure the times are in the correct order
    cdef double[:] start_times= np.sort(np.asarray([ times[k][0] for k in range(len(times))], dtype=np.double), kind='quicksort')
    cdef double[:] end_times= np.sort(np.asarray([ times[k][1] for k in range(len(times))], dtype=np.double), kind='quicksort')

    cdef Py_ssize_t N = 0
    cdef Py_ssize_t k = 0
    for j in range(len(x)):
        if k == len(start_times) or x[j] < start_times[k]:
            fx[N] = x[j]
            fy[N] = y[j]
            N += 1

        elif x[j] >= end_times[k]:
            k += 1
            if k < len(start_times) and x[j] < start_times[k]:
                fx[N] = x[j]
                fy[N] = y[j]
                N += 1

    return fx[:N], fy[:N]
