from MuonDataLib.data.events.detector import Detector
import numpy as np


def filter_data(data_list, condition):
    """
    A simple function for filtering a series
    of lists based on the same condition.
    :param data_list: the list of lists to filter.
    :param condition: the filter condition.
    :returns: a list of filtered data.
    """
    indicies = np.where(condition)[0]

    return [np.asarray(data)[indicies] for data in data_list]


class Instrument(object):
    """
    An Instrument is made up of multiple detectors.
    Each Instrument represents a single run.

    Methods:
    - set_bins: set the bins for the histograms.
    - get_histograms: gets the histogram values and bin edges.
    - add_new_frame: adds a new frame to all of the detectors.
    - add_event_data: sorts and adds event data to each detector.
    """
    def __init__(self, start_time, N_det=64):
        """
        Creates an instrument object.
        By default the bins are 0.5 micro seconds.
        :param start_time: this is the date value for the start of the run.
        :param N_det: the number of detectors (default 64)
        """
        self.N_det = N_det
        self._detectors = [Detector(j) for j in range(self.N_det)]
        self._start = start_time
        # need to start counting from 0 after increment
        self._current_frame = -1
        self._current_index = None
        self._bounds = [0, 30]
        self.set_bins(.5)
        # ns to micro sec
        self._unit_conversion = 1.e-3

    def set_bins(self, bin_width):
        """
        Sets bin edges to a constant width from 0 to 30 micro sec.
        :param bin_width: the bin width to use when calculating the
        bin edges.
        """
        self._bin_edges = np.arange(self._bounds[0],
                                    self._bounds[1] + bin_width,
                                    bin_width)

    def get_histogram(self, ID):
        """
        Gets the histogram data for a single detector.
        :param ID: the detector ID to get the histogram for.
        :returns: the heights and bin edges for the histogram.
        """
        return self._detectors[ID].get_histogram(self._bin_edges,
                                                 self._unit_conversion)

    def add_new_frame(self, start_time, period, index):
        """
        Adds a new frame to all of the detectors.
        :param start_time: the start time for the new frame.
        :param period: the period of the new frame.
        :param index: the event index that the new frame starts at.
        """
        self._current_frame += 1
        self._current_index = index
        for j, _ in enumerate(self._detectors):
            self._detectors[j].add_new_frame(start_time, period)

    def add_event_data(self,
                       IDs,
                       all_times,
                       all_amps,
                       periods,
                       start_times,
                       start_indicies):
        """
        Adds event data to the correct frame and detector.
        :param IDs: the detector IDs
        :param all_times: all of the event time stamps.
        :param all_amps: all of the event amplitudes.
        :param periods: all of the periods.
        :param start_times: the start times for the frames.
        :param start_indicies: the index of first event for each frame.
        """
        # list of start indicies for active and new frames
        condition = np.asarray(start_indicies) >= self._current_index
        frame_list, starts, p = filter_data([start_indicies,
                                             start_times,
                                             periods],
                                            condition)

        # loop over frames
        for k in range(len(frame_list)-1):
            current = frame_list[k]
            next_frame = frame_list[k + 1]
            self._add_data(self._current_frame,
                           IDs[current: next_frame],
                           all_times[current: next_frame],
                           all_amps[current: next_frame])
            # will always be a next frame in this loop
            self.add_new_frame(starts[k+1],
                               p[k+1],
                               frame_list[k+1])
        # load data for current frame
        self._add_data(self._current_frame, IDs[self._current_index:],
                       all_times[frame_list[-1]:],
                       all_amps[frame_list[-1]:])

    def _add_data(self, frame, IDs, times, amps):
        """
        Adds event data to the detectors.
        This will filter events to the correct detector.
        :param frame: the frame number to add events to.
        :param IDs: the detector ID list for the events.
        :param times: the event time stamps.
        :param amps: the event amplitudes.
        """
        for j, _ in enumerate(self._detectors):
            # get indicies for the current detector
            indicies = np.where(np.asarray(IDs) == j)[0]
            self._detectors[j].add_events_to_frame(frame,
                                                   np.asarray(times)[indicies],
                                                   np.asarray(amps)[indicies])
