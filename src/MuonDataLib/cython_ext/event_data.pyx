from MuonDataLib.cython_ext.stats import make_histogram
from MuonDataLib.cython_ext.filter import (get_indices,
                                           rm_overlaps,
                                           good_values_ints,
                                           good_values_double)
import numpy as np
import json
import time
cimport numpy as cnp
import cython
cnp.import_array()


cdef class Events:
    """
    Class for storing event information
    """
    cdef public int [:] IDs
    cdef public double[:] times
    cdef readonly int N_spec
    cdef readonly int[:] start_index_list
    cdef readonly int[:] end_index_list
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
        return np.asarray(self.frame_start_time)*1e-9

    def _get_filters(self):
        """
        A method to get the filters for testing
        :returns: the filter dicts
        """
        return self.filter_start, self.filter_end

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
        # can add check for filter
        cdef int[:] IDs, f_i_start, f_i_end
        cdef int frames = len(self.start_index_list)
        cdef double[:] times, f_start, f_end

        if len(self.filter_start.keys())>0:
            # sort the filter data
            f_start = np.sort(np.asarray(list(self.filter_start.values()), dtype=np.double), kind='quicksort')
            f_end = np.sort(np.asarray(list(self.filter_end.values()), dtype=np.double), kind='quicksort')

            # calculate the frames that are excluded by the filter
            f_i_start, f_i_end = get_indices(self.get_start_times(), f_start, f_end)
            f_i_start, f_i_end, rm_frames = rm_overlaps(f_i_start, f_i_end)
            # update the number of frames for the histogram
            frames -= rm_frames
            # remove the filtered data from the event lists
            IDs = good_values_ints(f_i_start, f_i_end, self.start_index_list, self.IDs)
            times = good_values_double(f_i_start, f_i_end, self.start_index_list, self.times)
        else:
            IDs = self.IDs
            times = self.times


        hist, bins = make_histogram(times,
                                    IDs,
                                    self.N_spec,
                                    min_time,
                                    max_time,
                                    width)
        if cache is not None:
            cache.save(np.asarray([hist]), bins,
                       np.asarray([frames], dtype=np.int32))

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

