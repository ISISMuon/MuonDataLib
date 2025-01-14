import numpy as np
cimport numpy as cnp
import cython
cimport cpython.datetime as dt
cnp.import_array()


cdef class EventsCache:
    """
    A simple class for caching the event data into histograms

    *********************************************************
    WARNING:

    This class may not take multi period data into account
    beyond allowing unit tests to pass
    *********************************************************

    """
    cdef readonly int[:, :, :] histograms
    cdef readonly double[:] bins
    cdef readonly int[:] N_frames
    cdef readonly int[:] N_good_frames
    cdef readonly int[:] N_requested_frames
    cdef readonly int[:] rm_frames
    cdef readonly dt.datetime start_time
    cdef readonly dt.datetime end_time

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
        self.N_frames = np.asarray([], dtype=np.int32)
        self.N_good_frames = np.asarray([], dtype=np.int32)
        self.N_requested_frames = np.asarray([], dtype=np.int32)
        self.rm_frames = np.asarray([], dtype=np.int32)
        self.start_time = dt.datetime(2018, 12, 24, 13, 32, 1)
        self.end_time = dt.datetime(2018, 12, 25, 14, 42, 10)

    def test(self, seconds):
        t = dt.timedelta(seconds=seconds)
        print(self.start_time, t)
        return self.start_time + t

    def save(self,
            int[:, :, :] histograms,
            double[:] bins,
            int[:] N_frames):#,
            #int[:] rm_frames,
            #double start_time,
            #double end_frame_time):
        """
        Store data in the cache
        :param histograms: the histogram data (periods, N_det, bin)
        :param bins: the histogram bins
        :param N_frames: the number of frames used (can be an int of list)
        :param rm_frames: the number of frames removed
        (at present doesnt account for multiperiod data)
        :param start_time: the start time
        :param end_frame_time: the last frame start time
        """
        self.histograms = histograms
        self.bins = bins
        self.N_frames = N_frames
        self.N_good_frames = N_frames
        self.N_requested_frames = N_frames
        #self.rm_frames = rm_frames
        #self.start_time = start_time
        # add 32 micro sec to the end of the last frame (ns)
        #self.end_time = end_frame_time + 32.0e3

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

    def set_good_frames(self, int[:] N):
        """
        :param N: the number of good frames
        """

        if len(N) != len(self.N_good_frames):
            raise RuntimeError(f"The number of good frames {N} "
                               "must be the same length as number "
                               "of frames {self.N_frames}")
        self.N_good_frames = N

    def get_good_frames(self):
        """
        :return: the number of good frames
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get frames")
        return self.N_good_frames

    def set_requested_frames(self, int[:] N):
        """
        :param N: the number of requested frames
        """

        if len(N) != len(self.N_good_frames):
            raise RuntimeError(f"The number of requested frames {N} "
                               "must be the same length as number "
                               "of frames {self.N_frames}")
        self.N_requested_frames = N

    def get_requested_frames(self):
        """
        :return: the number of good frames
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get frames")
        return self.N_requested_frames

    def empty(self):
        """
        Check if the cache is empty
        :return: if the cache is empty as a bool
        """
        if len(self.N_frames)==0:
            return True
        return False
