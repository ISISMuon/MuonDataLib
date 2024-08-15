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

    def __init__(self,
                 cnp.ndarray[int] IDs,
                 cnp.ndarray[double] times,
                ):
        """
        Creates an event object.
        This knows everything needed for the events to create a histogram.
        :param IDs: the detector ID's for the events
        :param times: the time stamps for the events, relative to the start of their frame
        """
        self.IDs = IDs
        # add as IDs counts from 0
        self.N_spec = np.max(IDs) + 1
        self.times = times

    def histogram(self,
                  frame_filter=None,
                  min_time=0,
                  max_time=32.768,
                  width=0.016):
        """
        Create a matrix of histograms from the event data
        :param filters: the filters to be applied
        :param min_time: the time for the first bin edge
        :param max_time: the time for the last bin edge
        :param width: the bin width
        :returns: a matrix of histograms, bin edges
        """
        if frame_filter is not None:
            times = frame_filter.apply_filter(self.times)
            IDs = frame_filter.apply_filter(self.IDs)
            return make_histogram(times, IDs, self.N_spec,
                                  min_time, max_time, width)

        return make_histogram(self.times, self.IDs, self.N_spec,
                              min_time, max_time, width)

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
