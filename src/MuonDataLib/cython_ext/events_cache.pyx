import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()


cdef class EventsCache:
    """
    A simple class for caching the event data into histograms
    """
    cdef readonly int[:, :, :] histograms
    cdef readonly double[:] bins
    cdef readonly int N_frames

    def __init__(self):
        """
        Create an empty cache
        """
        self.clear()

    def clear(self):
        """
        Clear all data from the cache
        """
        self.histograms = None
        self.bins = None
        self.N_frames = 0

    def save(self,
            int[:, :, :] histograms,
            double[:] bins,
            int N_frames):
        """
        Store data in the cache
        :param histograms: the histogram data (periods, N_det, bin)
        :param bins: the histogram bins
        :param N_frames: the number of frames used
        """
        self.histograms = histograms
        self.bins = bins
        self.N_frames = N_frames

    def get_histograms(self):
        """
        :return: the stored histograms and bins
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get histograms")
        return np.asarray(self.histograms), np.asarray(self.bins)

    def get_total_frames(self):
        """
        :return: the total number of frames
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get frames")
        return self.N_frames

    def empty(self):
        """
        Check if the cache is empty
        :return: if the cache is empty as a bool
        """
        if self.N_frames==0:
            return True
        return False
