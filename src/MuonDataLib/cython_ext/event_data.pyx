from MuonDataLib.cython_ext.stats import make_histogram
import numpy as np
import time
cimport numpy as cnp
import cython
cnp.import_array()


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
        # add as IDs counts from 0
        self.N_spec = np.max(IDs) + 1
        self.times = times
        self.start_index_list = start_i
        self.end_index_list = np.append(start_i[1:], len(IDs))
        #self.frame_start_time = frame_time

    def histogram(self):
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


def mock_events():
    IDs = np.asarray([0, 1, 0, 1, 0, 1], dtype='int32')
    time = np.asarray([1., 2., 1., 2., 1., 2.], dtype=np.double)
    frame_i = np.asarray([0, 3], dtype='int32')
    events = Events(IDs,
                    time,
                    frame_i)
    return IDs, time, frame_i, events


