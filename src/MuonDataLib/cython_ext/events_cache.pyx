import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()


cdef class EventsCache:
    cdef readonly int[:, :, :] histograms
    cdef readonly double[:] bins
    cdef readonly int N_frames

    def __init__(self):
        self.clear()

    def clear(self):
        self.histograms = None
        self.bins = None
        self.N_frames = 0

    def save(self,
            int[:, :, :] histograms,
            double[:] bins,
            int N_frames):
        self.histograms = histograms
        self.bins = bins
        self.N_frames = N_frames

    def get_histograms(self):
        return np.asarray(self.histograms), np.asarray(self.bins)

    def get_total_frames(self):
        return self.N_frames

    def empty(self):
        if self.N_frames==0:
            return True
        return False

    def print(self):
        print(np.asarray(self.histograms))
        print(np.asarray(self.bins))
        print(self.N_frames)

