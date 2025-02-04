from MuonDataLib.data.utils import NONE
from MuonDataLib.cython_ext.stats import make_histogram
from MuonDataLib.cython_ext.filter import (cf_less,
                                           cf_greater,
                                           remove_data,
                                           keep_data,
                                           get_indices,
                                           rm_overlaps,
                                           good_values_ints,
                                           good_values_double)
import numpy as np
import json
import time
cimport numpy as cnp
import cython
cnp.import_array()


cdef double ns_to_s = 1.e-9


cdef class Events:
    """
    Class for storing event information
    """
    cdef public int [:] IDs
    cdef public double[:] times
    cdef readonly int N_spec
    cdef public int[:] start_index_list
    cdef public int[:] end_index_list
    cdef readonly dict[str, double] filter_start
    cdef readonly dict[str, double] filter_end
    cdef readonly double[:] frame_start_time


    def __init__(self,
                 cnp.ndarray[int] IDs,
                 cnp.ndarray[double] times,
                 cnp.ndarray[int] start_i,
                 cnp.ndarray[double] frame_start,
                 int N_det):
        """
        Creates an event object.
        This knows everything needed for the events to create a histogram.
        :param IDs: the detector ID's for the events
        :param times: the time stamps for the events, relative to the start of their frame
        :param start_i: the first event index for each frame
        :param frame_start: the start time for the frames
        :param N_det: the number of detectors
        """
        self.IDs = IDs
        self.N_spec = N_det
        self.times = times
        self.start_index_list = start_i
        self.end_index_list = np.append(start_i[1:], np.int32(len(IDs)))
        self.frame_start_time = frame_start
        self.filter_start = {}
        self.filter_end = {}

    def get_start_times(self):
        """
        Get the frame start times (stored in ns)
        :returns: the frame start times in seconds
        """
        return np.asarray(self.frame_start_time)

    def _get_filters(self):
        """
        A method to get the filters for testing
        :returns: the filter dicts
        """
        return self.filter_start, self.filter_end

    def apply_log_filter(self, str name, double[:] x, double[:] y, double min_filter, double max_filter):
        status = False

        cdef Py_ssize_t j, N
        N = 0
        cdef cnp.ndarray[int] start = np.zeros(len(x), dtype=np.int32)
        cdef cnp.ndarray[int] stop = np.zeros(len(x), dtype=np.int32)

        if (min_filter is not NONE and y[0] < min_filter or
            max_filter is not NONE and y[0] > max_filter):
            status = True
            start[0] = 0

        less = cf_less()
        greater = cf_greater()

        for j in range(1, len(y)):
            if (remove_data(min_filter, status, y[j], less) or
                remove_data(max_filter, status, y[j], greater)):
                status = True
                # since it crosses before the current value
                start[N] = j-1
            elif (keep_data(min_filter, status, y[j], greater) and
                  keep_data(max_filter, status, y[j], less)):
                status = False
                stop[N] = j
                N += 1

        # if its on, turn it off
        if status:
            stop[N] = len(y) - 1
            N += 1

        for j in range(N):
            self.add_filter(f'name_{j}', x[start[j]]/ns_to_s,
                            x[stop[j]]/ns_to_s)

        #########
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        for j in range(N):
            x1.append(x[start[j]])
            y1.append(y[start[j]])
            x2.append(x[stop[j]])
            y2.append(y[stop[j]])
        return x1, y1, x2, y2


    def add_filter(self, str name, double start, double end):
        """
        Adds a time filter to the events
        The times are in the same units as the stored events
        :param name: the name of the filter
        :param start: the start time for the filter
        :param end: the end time for the filter
        """
        if name in self.filter_start.keys():
            raise RuntimeError(f'The filter {name} already exists')
        self.filter_start[name] = start
        self.filter_end[name] = end

    def remove_filter(self, str name):
        """
        Remove a time filter from the events
        :param name: the name of the filter to remove
        """
        if name not in self.filter_start.keys():
            raise RuntimeError(f'The filter {name} does not exist')
        del self.filter_start[name]
        del self.filter_end[name]

    def clear_filters(self):
        """
        A method to clear all of the time filters
        """
        self.filter_start.clear()
        self.filter_end.clear()

    def report_filters(self):
        """
        A simple method to create a more readable form for the
        user to inspect.
        :return: a dict of the filters, with start and end values.
        """
        data = {}
        for key in self.filter_start.keys():
            data[key] = (self.filter_start[key], self.filter_end[key])
        return data

    def load_filters(self, str file_name):
        """
        A method to filters from a json file.
        This will apply all of the filters from the file.
        :param file_name: the name of the json file
        """
        with open(file_name, 'r') as file:
            data = json.load(file)

        for key in data.keys():
            self.add_filter(key, *data[key])

    def save_filters(self, str file_name):
        """
        A method to save the current filters to a file.
        :param file_name: the name of the json file to save to.
        """
        data = self.report_filters()
        with open(file_name, 'w') as file:
            json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=4)

    @property
    def get_total_frames(self):
        return len(self.start_index_list)

    def _get_filtered_data(self, frame_times):
        """
        A method to get the information about the applied filters.
        This includes the list of events after the filter has been applied,
        the number of removed frames and the indices for the filters.
        :param frame_times: the times for the start of each frame (in seconds).
        The number of removed frames. The list of filtered detector IDs and
        event time stamps.
        """

        cdef int[:] IDs, f_i_start, f_i_end
        cdef int rm_frames = 0
        cdef double[:] times, f_start, f_end

        if len(self.filter_start.keys())>0:
            # sort the filter data
            f_start = np.sort(np.asarray(list(self.filter_start.values()), dtype=np.double), kind='quicksort')
            f_end = np.sort(np.asarray(list(self.filter_end.values()), dtype=np.double), kind='quicksort')

            # calculate the frames that are excluded by the filter
            f_i_start, f_i_end = get_indices(frame_times,
                                             ns_to_s*np.asarray(f_start),
                                             ns_to_s*np.asarray(f_end),
                                             'frame start time',
                                             'seconds')
            f_i_start, f_i_end, rm_frames = rm_overlaps(f_i_start, f_i_end)
            # remove the filtered data from the event lists
            IDs = good_values_ints(f_i_start, f_i_end, self.start_index_list, self.IDs)
            times = good_values_double(f_i_start, f_i_end, self.start_index_list, self.times)
        else:
            # no filters
            IDs = self.IDs
            times = self.times
            f_i_start = np.asarray([], dtype=np.int32)
            f_i_end = np.asarray([], dtype=np.int32)

        return f_i_start, f_i_end, rm_frames, IDs, times

    """
    def filter_log(self, f_i_start, f_i_end, log_x, log_y):
        new_x = np.zeros(len(log_x))
        new_y = np.zeros(len(log_y))

        N = 0
        record = True
        if log_x[0] > self.start_index_list[f_i_start]:
            record = False

        for j in range(len(log_x)):
            if record and log_x[j]
    """
    def histogram(self,
                  double min_time=0.,
                  double max_time=32.768,
                  double width=0.016,
                  cache=None):
        """
        Create a matrix of histograms from the event data
        and apply any filters that might be present.
        :param min_time: the start time for the histogram
        :param max_time: the end time for the histogram
        :param width: the bin width for the histogram
        :param cache: the cache of event data histograms
        :returns: a matrix of histograms, bin edges
        """
        cdef int[:] IDs, f_i_start, f_i_end
        cdef int rm_frames = 0
        cdef double[:] times

        cdef double[:] frame_times = ns_to_s*np.asarray(self.get_start_times())

        f_i_start, f_i_end, rm_frames, IDs, times = self._get_filtered_data(frame_times)

        hist, bins = make_histogram(times,
                                    IDs,
                                    self.N_spec,
                                    min_time,
                                    max_time,
                                    width)
        if cache is not None:

            first_time, last_time = self._start_and_end_times(frame_times,
                                                              f_i_start,
                                                              f_i_end)
            cache.save(np.asarray([hist]), bins,
                       np.asarray([rm_frames], dtype=np.int32),
                       veto_frames=np.zeros(1, dtype=np.int32),
                       first_time=first_time,
                       last_time=last_time,
                       resolution=width)

        return hist, bins

    @staticmethod
    def _start_and_end_times(double[:] frame_times,
                             int[:] f_i_start,
                             int[:] f_i_end):
        """
        A method to get the start and end time for the filtered
        data. Each frame at best contains about 20ms of events
        and these will always be at the start of the frame.
        So if the beam goes down, the next frame could be an hour
        later but the events will all be within the
        first 20ms of the frame. Therefore,
        we can estimate the end time by using the time passed
        between the start time and the time stamp for the start
        of the last frame. Since the 20ms will make little
        difference to the end tiime as a first order approximation
        (we only record to an accuracy of seconds). The start time
        is from the first frame that is included in the filtered
        data.
        :param frame_times: the timestamps for the start of the
        frames.
        :param f_i_start: the list of indices for the start
        of the filters.
        :param f_i_end: the list of indices for the end
        of the filters
        :returns: the start and end times for the filtered data
        """
        cdef double first_time, last_time
        # no filters
        if len(f_i_start) == 0:
            return frame_times[0], frame_times[-1]

        if f_i_start[0] > 0:
            # if first filter is after first frame
            first_time = frame_times[0]
        else:
            # the first filter includes first frame
            first_time = frame_times[f_i_end[0] + 1]

        if f_i_end[-1] < len(frame_times)-1:
            # if the last filter is before the last frame
            last_time = frame_times[-1]
        else:
            """
            If the last filter includes the last frame.
            Want to get the time of the frame just
            before the last filter starts.
            Hence, f_i_start[-1] - 1.
            """
            last_time = frame_times[f_i_start[-1] - 1]
        return first_time, last_time

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

