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

    def __init__(self,
                 cnp.ndarray[int] IDs,
                 cnp.ndarray[double] times,
                 cnp.ndarray[int] start_i,
                 int N_det):
        """
        Creates an event object.
        This knows everything needed for the events to create a histogram.
        :param IDs: the detector ID's for the events
        :param times: the time stamps for the events, relative to the start of their frame
        :param start_i: the first event index for each frame
        :param N_det: the number of detectors
        """
        self.IDs = IDs
        self.N_spec = N_det
        self.times = times
        self.start_index_list = start_i
        self.end_index_list = np.append(start_i[1:], np.int32(len(IDs)))
        #self.frame_start_time = frame_time

    @property
    def get_total_frames(self):
        return len(self.start_index_list)

    def histogram(self,
                  double min_time=0.,
                  double max_time=32.768,
                  double width=0.016,
                  cache=None):
        """
        Create a matrix of histograms from the event data
        :param min_time: the start time for the histogram
        :param max_time: the end time for the histogram
        :param width: the bin width for the histogram
        :param cache: the cache of event data histograms
        :returns: a matrix of histograms, bin edges
        """
        hist, bins = make_histogram(self.times,
                                    self.IDs,
                                    self.N_spec,
                                    min_time,
                                    max_time,
                                    width)
        if cache is not None:
            cache.save(np.asarray([hist]), bins,
                       np.asarray([len(self.start_index_list)], dtype=np.int32))
        return hist, bins

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

