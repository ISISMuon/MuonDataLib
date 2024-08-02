import h5py
from MuonDataLib.cython_ext.add import load_data
import numpy as np
import time
cimport numpy as cnp
import cython
cnp.import_array()


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef make_histogram(
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


cdef class Events:
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
        return make_histogram(self.times, self.IDs, self.N_spec)

    @property
    def get_N_spec(self):
        """
        :return: the number of spectra/detectors
        """
        return self.N_spec

    @property
    def get_N_events(self):
        """
        :return: the number of spectra/detectors
        """
        return len(self.IDs)

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



def load_data(file_name):
        """
        Loads the data from a file
        :param file_name: the name of the event nxs file to load
        :return: the time to run this method, the total number of events
        """
        start = time.time()
        IDs, frames, times, amps, frame_times = _load_data(file_name)
        events = Events(IDs, times, frames)
        return time.time() - start, events


def _load_data(file_name):
        """
        Loads event data from the event nxs file.
        :param file_name: the name of the file to load.
        :return: IDs, first index for frame, time stamps,
        amplitudes, time at the start of the frame
        """

        with h5py.File(file_name, 'r') as file:
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

