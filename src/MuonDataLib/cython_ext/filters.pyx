import numpy as np
cimport numpy as cnp
import cython
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.algorithm cimport sort as sort
cnp.import_array()


cdef vector[double] my_sort(vector[double] times):
    """
    A simple wrapper for a vector sort
    :param times: the times of the data to be sorted
    :return: a sorted list of time
    """
    sort(times.begin(), times.end())
    return times


cdef class FrameFilter:
    """
    A class for filtering out frames.
    If any part of the frame is within the filter,
    then it is excluded.
    """
    cdef readonly cnp.int32_t[:] start_index_list
    cdef readonly cnp.int32_t[:] end_index_list
    cdef readonly double[:] frame_start_time
    cdef readonly vector[double] filter_start_time
    cdef readonly vector[double] filter_end_time
    cdef readonly list names


    def __init__(self,
                 cnp.ndarray[int] start_i,
                 cnp.ndarray[double] frame_time,
                 int data_end):
        """
        Create the frame filter object
        :param start_i: the start indicies for the frames
        :param frame_time: the time at the start of each time
        :param data_end: the index of the end of the event data
        """
        self.start_index_list = start_i
        self.end_index_list = np.append(start_i[1:] - 1, np.int32(data_end))
        self.frame_start_time = frame_time
        # create some empty filter info
        self.names = []
        self.filter_start_time = []
        self.filter_end_time = []


    def add_filter(self, str name, double start, double end):
        """
        Add a single filter to the object.
        :param name: the name of the filter
        :param start: the start time for the filter
        :param end: the end time for the filter
        """
        self.names.append(name)
        self.filter_start_time.push_back(start)
        self.filter_end_time.push_back(end)

    @property
    def get_filters(self):
        """
        :return: a dict of the filters {name: (start, end)}
        """
        filters = {}
        for k in range(self.filter_start_time.size()):
            filters[self.names[k]] = (self.filter_start_time[k],
                                      self.filter_end_time[k])
        return filters

    def apply_filter(self, data):
        """
        Applys the filter to an array.
        i.e. it removes the data in the relevant frames.
        :param data: the input data to filter
        :return: an array of data excluding the filtered data
        """
        exclude = self.filter_data()

        tmp = np.asarray(data)
        for j in range(len(exclude)-1, 0, -2):
            tmp = tmp[np.r_[:exclude[j-1], exclude[j] + 1: len(tmp)]]
        return tmp

    def filter_data(self):
        """
        Filters the data
        """
        # sanity check
        if self.filter_start_time.size() == 0:
            return

        # get ordered filter times
        filter_start_time = my_sort(self.filter_start_time)
        filter_end_time = my_sort(self.filter_end_time)

        cdef vector[double] exclude = []
        exclude.push_back(filter_start_time[0])
        current_end = filter_end_time[0]
        start = filter_start_time[0]
        end = filter_end_time[0]

        for k in range(1, filter_start_time.size()):
            start = filter_start_time[k]
            # if end < start => no overlap
            if end < start:
                exclude.push_back(end)
                exclude.push_back(start)
            # update with new filter window
            end = filter_end_time[k]
        exclude.push_back(filter_end_time[filter_end_time.size() - 1])


        # get filtered times in terms of events
        rm_index = []
        filter_index = 0
        start_filter = exclude[0]
        end_filter = exclude[1]

        time = self.frame_start_time[0]
        time_index = 0
        for k in range(0, len(exclude),2):
            start_filter = exclude[k]
            end_filter = exclude[k + 1]
            in_frame = False
            for j in range(time_index, len(self.frame_start_time)-1):
                frame_start = self.frame_start_time[j]
                frame_end = self.frame_start_time[j + 1]
                # start filter is in frame
                if start_filter >= frame_start and start_filter < frame_end and not in_frame:
                    rm_index.append(self.start_index_list[j])
                    in_frame = True
                    if end_filter < frame_end:
                        rm_index.append(self.end_index_list[j])
                        time_index = j + 1
                        break
                # end filter is nolonger in frame
                elif in_frame and end_filter < frame_end:
                    time_index = j + 1
                    rm_index.append(self.end_index_list[j])
                    break

        return rm_index
