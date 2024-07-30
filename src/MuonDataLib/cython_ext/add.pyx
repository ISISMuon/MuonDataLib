import h5py
import numpy as np
import time
cimport numpy as cnp
import cython
from cython.parallel import prange
from cython.parallel cimport parallel
cimport openmp
cnp.import_array()
#

def my_add(int a, int b):
    return a + b


def load_data(file_name):
    """
    Loads event data.
    :param file_name: the name of the file to load.
    """
    start_timer = time.time()

    file = h5py.File(file_name, 'r')
    tmp = file.require_group('raw_data_1')
    tmp = tmp.require_group('detector_1')

    cdef int N = tmp['event_id'].len()

    cdef cnp.ndarray[int, ndim=1] IDs = np.zeros(N, dtype=int)
    cdef cnp.ndarray[double, ndim=1] times = np.zeros(N, dtype=np.double)
    cdef cnp.ndarray[double, ndim=1] amps = np.zeros(N, dtype=np.double)

    tmp['event_id'].read_direct(IDs)
    tmp['event_time_offset'].read_direct(times)
    tmp['pulse_height'].read_direct(amps)

    M = tmp['event_index'].len()

    cdef cnp.ndarray[int, ndim=1] start_j = np.zeros(M, dtype=int)
    tmp['event_index'].read_direct(start_j)


    cdef cnp.ndarray[double, ndim=1] start_t = np.zeros(M, dtype=np.double)
    tmp['event_time_zero'].read_direct(start_t)

    #periods = np.asarray(tmp['period_number'][:])
    file.close()

    return time.time() - start_timer, IDs, start_j, times, amps, start_t

def load_data_auto(file_name):
    """
    Loads event data.
    :param file_name: the name of the file to load.
    """
    start_timer = time.time()

    cdef int N, M
    cdef cnp.ndarray[int, ndim=1] IDs
    cdef cnp.ndarray[double, ndim=1] times
    cdef cnp.ndarray[double, ndim=1] amps
    cdef cnp.ndarray[int, ndim=1] start_j
    cdef cnp.ndarray[double, ndim=1] start_t

    cdef list[str] data =['event_id',
                           'event_time_offset',
                           'pulse_height',
                           'event_index',
                           'event_time_zero']
    cdef int N_data = len(data)

    with h5py.File(file_name, 'r') as file:
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('detector_1')

        N = tmp['event_id'].len()

        IDs = np.zeros(N, dtype=int)
        times = np.zeros(N, dtype=np.double)
        amps = np.zeros(N, dtype=np.double)

        M = tmp['event_index'].len()
        start_j = np.zeros(M, dtype=int)
        start_t = np.zeros(M, dtype=np.double)

        for i in range(N_data):
            if data[i] == 'event_id':
                tmp['event_id'].read_direct(IDs)
            elif data[i] == 'event_time_offset':
                tmp['event_time_offset'].read_direct(times)
            elif data[i] == 'pulse_height':
                tmp['pulse_height'].read_direct(amps)
            elif data[i] == 'event_index':
                tmp['event_index'].read_direct(start_j)
            elif data[i] == 'event_time_zero':
                tmp['event_time_zero'].read_direct(start_t)

        #periods = np.asarray(tmp['period_number'][:])
    file.close()

    return time.time() - start_timer, IDs, start_j, times, amps, start_t

"""
being bad
"""

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef hist(cnp.ndarray[unsigned long, ndim=1] IDs,
          cnp.ndarray[unsigned long, ndim=1] times,
          cnp.ndarray[int, ndim=1] frame_start,
          cnp.ndarray[int, ndim=1] frame_end,
          int N):

    #print(IDs)
    #print(times)
    #print(frame_start)
    #print(frame_end)
    #print(N)
    cdef Py_ssize_t N_f = len(frame_start)
    cdef Py_ssize_t det, k, j_bin, j
    cdef double width = 0.5
    cdef double max_time = 30.

    # need a better way to make sure we get all bins
    # need to add code to return just a section of the histogram

    cdef cnp.ndarray[double, ndim=1] bins = np.arange(0, max_time + width, width, dtype=np.double)
    cdef cnp.ndarray[double, ndim=2] result = np.zeros((N+1, len(bins)-1), dtype=np.double)
    cdef double[:, :] mat = result
    #print(bins)
    #print(result)
    #print('start')
    for j in range(N_f):
        for k in range(frame_start[j], frame_end[j]):
            det = IDs[k]
            if times[k] > max_time:
                continue
            elif times[k] > 0:
                j_bin = int((1e-3*times[k]) // width)
            else:
                j_bin = 0
            mat[det, j_bin] += 1. / width
    #parint("done")
    return result, bins


class Events(object):
    def __init__(self):
        self._det = []
        self._data = {}
        self._N = 0
        return

    # want to try and do det and then frames ...
    def histogram(self):
        bins = np.arange(0, 30.5, .5)

        return hist(self._data['IDs'], self._data['times'], self._data['frame start'],
                    self._data['frame end'], self._N)

    def set_data(self, IDs, times, amps, N, frames, dt):
        self._dt = dt
        self._data['IDs'] = IDs
        self._data['times'] = times
        self._data['frame start'] = []
        self._data['frame end'] = []
        for k in range(len(frames)-1):
            self._data['frame start'].append(frames[k])
            self._data['frame end'].append(frames[k+1])
        self._data['frame start'].append(frames[len(frames)-1])
        self._data['frame end'].append(len(IDs))

        self._data['frame start'] = np.asarray(self._data['frame start'], dtype=int)
        self._data['frame end'] = np.asarray(self._data['frame end'], dtype=int)

    def load_data(self, file_name):
        IDs, frames, times, amps, frame_times = self._load_data(file_name)
        N = np.max(IDs)
        start = time.time()
        dt = frame_times[1] - frame_times[0]
        self.set_data(IDs, times, amps, N, frames, dt)

        return time.time() - start, len(IDs)

    def _load_data(self, file_name):
        """
        Loads event data.
        :param file_name: the name of the file to load.
        """
        self._file_name = file_name
        start_timer = time.time()
        with h5py.File(self._file_name, 'r') as file:
            tmp = file.require_group('raw_data_1')
            tmp = tmp.require_group('detector_1')

            IDs = np.asarray(tmp['event_id'][:])
            start_indicies = np.asarray(tmp['event_index'][:])
            times = np.asarray(tmp['event_time_offset'][:])
            start_times = np.asarray(tmp['event_time_zero'][:])
            #periods = np.asarray(tmp['period_number'][:])
            amps = np.asarray(tmp['pulse_height'][:])
            #start = tmp['event_time_zero'].attrs['offset'][0]

        self._N = np.max(IDs)
        self.h5py_time = time.time() - start_timer

        return IDs, start_indicies, times, amps, start_times
    """
    def load_data(self, file_name):
        load_time, IDs, frames, times, amps, frame_times = load_data_auto(file_name)
        print("boo")
        N = np.max(IDs)
        print("N", N)
        dt = frame_times[1] - frame_times[0]
        print("dt", dt)
        self.set_data(IDs, times, amps, N, frames, dt)
        print("set")
        return load_time, len(IDs)

    """

