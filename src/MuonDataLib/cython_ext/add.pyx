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

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef hist2(
        double[:] times,
        cnp.int32_t[:] spec,
        int N_spec):
    """
    This method creates histograms from a list of data.
    It produces a matrix of histograms for multiple spectra.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :returns: a matrix of histograms, the bin edges
    """

    cdef Py_ssize_t det, k, j_bin

    cdef double width = 0.5
    cdef double min_time = 30.
    cdef double max_time = 30.

    cdef cnp.ndarray[double, ndim=1] bins = np.arange(min_time, max_time + width, width, dtype=np.double)
    cdef cnp.ndarray[double, ndim=2] result = np.zeros((N_spec+1, len(bins)-1), dtype=np.double)
    cdef double[:, :] mat = result

    for k in range(len(times)):
        det = spec[k]
        if times[k] <= max_time and times[k] >= min_time:
            j_bin = int((1e-3*(times[k] - min_time)) // width)
            mat[det, j_bin] += 1. / width
    return result, bins


cdef class my_events:
    """
    Class for storing event information
    """
    cdef public cnp.int32_t[:] IDs
    cdef public double[:] times
    cdef readonly int N_spec
    cdef readonly cnp.int32_t[:] start_index_list
    cdef readonly cnp.int32_t[:] end_index_list
    #cdef readonly cnp.ndarray[int] frame_start_time

    def __init__(self,
                 cnp.ndarray[int] IDs,
                 cnp.ndarray[double] times,
                 cnp.ndarray[int] start_i): #, frame_time):
        """
        Creates an event object.
        This knows everything needed for the events to create a histogram.
        :param IDs: the detector ID's for the events
        :param times: the time stamps for the events, relative to the start of their frame
        :param start_i: the first event index for each frame
        """
        self.IDs = IDs
        self.N_spec = np.max(IDs)
        self.times = times
        self.start_index_list = start_i
        self.end_index_list = np.append(start_i[1:], len(IDs))
        #self.frame_start_time = frame_time

    def hist(self):
        """
        Create a matrix of histograms from the event data
        ;returns: a matrix of histograms, bin edges
        """
        return hist2(self.times, self.IDs, self.N_spec)

    @property
    def get_N_spec(self):
        """
        :return: the number of spectra/detectors
        """
        return self.N_spec

    @property
    def get_filtered_events(self):
        """
        Later this will apply filters.
        Either by adding subsets of the events, so to exclude the
        filteref out frames.
        Or by adding an offset to unwanted events (e.g. bad amplitudes)
        :return: the IDs for the events
        """
        return self.IDs



class test(object):
    """
    Workflow for loading event nxs data and creating histograms
    """
    def __init__(self):
        """
        Creates an empty load instance
        """
        self._stuff = None

    def load_data(self, file_name):
        """
        Loads the data from a file
        :param file_name: the name of the event nxs file to load
        :return: the time to run this method, the total number of events
        """
        start = time.time()
        IDs, frames, times, amps, frame_times = self._load_data(file_name)
        self._stuff = my_events(IDs, times, frames)
        return time.time() - start, len(IDs)

    def hist(self):
        """
        Create a matrix of histograms from the event data
        ;returns: a matrix of histograms, bin edges
        """
        return self._stuff.hist()


    def _load_data(self, file_name):
        """
        Loads event data from the event nxs file.
        :param file_name: the name of the file to load.
        :return: IDs, first index for frame, time stamps,
        amplitudes, time at the start of the frame
        """
        self._file_name = file_name

        with h5py.File(self._file_name, 'r') as file:
            tmp = file.require_group('raw_data_1')
            tmp = tmp.require_group('detector_1')

            N = tmp['event_id'].len()

            IDs = np.zeros(N, dtype=np.int32)
            times = np.zeros(N, dtype=np.double)
            amps = np.zeros(N, dtype=np.double)

            M = tmp['event_index'].len()
            start_j = np.zeros(M, dtype=np.int32)
            start_t = np.zeros(M, dtype=np.double)

            tmp['event_id'].read_direct(IDs)
            tmp['event_time_offset'].read_direct(times)
            tmp['pulse_height'].read_direct(amps)
            tmp['event_index'].read_direct(start_j)
            tmp['event_time_zero'].read_direct(start_t)

        return IDs, start_j, times, amps, start_t


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
        start = time.time()
        IDs, frames, times, amps, frame_times = self._load_data(file_name)
        N = np.max(IDs)
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

