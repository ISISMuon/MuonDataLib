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
    cdef readonly int[:] N_event_frames
    cdef readonly int[:] N_filter_frames
    cdef readonly int[:] N_veto_frames
    cdef readonly dt.datetime start_time

    def __init__(self, dt.datetime start_time, int[:] event_frames):
        """
        Create an empty cache
        """
        self.N_event_frames = event_frames
        self.start_time = start_time
        self.clear()

    def clear(self):
        """
        Clear all data from the cache
        """
        self.histograms = None
        self.bins = None
        self.N_filter_frames = np.asarray([], dtype=np.int32)
        self.N_veto_frames = np.asarray([], dtype=np.int32)

    def test(self, seconds):
        t = dt.timedelta(seconds=seconds)
        print(self.start_time, self.end_time)
        return self.start_time + t

    def save(self,
            int[:, :, :] histograms,
            double[:] bins,
            int[:] filter_frames,
            int[:] veto_frames):
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
        N = len(self.N_event_frames)
        if len(filter_frames) != N or len(veto_frames) != N:
            raise RuntimeError("The list of frames does not match")
        self.histograms = histograms
        self.bins = bins
        self.N_filter_frames = filter_frames
        self.N_veto_frames = veto_frames

    def get_histograms(self):
        """
        :return: the stored histograms and bins
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get histograms")
        return np.asarray(self.histograms), np.asarray(self.bins)

    def frame_check(self):
        """
        Check that the cache has data, if not return error
        """
        if self.empty():
            raise RuntimeError("The cache is empty, cannot get frames")

    @property
    def get_discarded_good_frames(self):
        """
        :return: the number of discarded good frames (filtered + veto)
        """
        self.frame_check()
        return np.asarray(self.N_filter_frames) + np.asarray(self.N_veto_frames)

    @property
    def get_discarded_raw_frames(self):
        """
        :return: the number of discarded raw frames (filtered)
        """
        self.frame_check()
        return np.asarray(self.N_filter_frames)

    @property
    def get_good_frames(self):
        """
        :return: the number of good frames
        """
        self.frame_check()
        return np.asarray(self.N_event_frames) - self.get_discarded_good_frames

    @property
    def get_raw_frames(self):
        """
        :return: the number of raw frames
        """
        self.frame_check()
        return np.asarray(self.N_event_frames) - self.get_discarded_raw_frames

    def empty(self):
        """
        Check if the cache is empty
        :return: if the cache is empty as a bool
        """
        if len(self.N_filter_frames)==0:
            return True
        return False

    @property
    def get_count_duration(self):
        """
        good frames * (100 ms)/4 then convert to seconds
        :return: the duration of the experiment, while on, in seconds
        """
        self.frame_check()
        return self.get_good_frames*0.025
