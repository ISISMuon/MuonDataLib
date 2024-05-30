from MuonDataLib.data.events.detector import Detector
import numpy as np


def filter_data(data_list, condition):
    indicies = np.where(condition)[0]

    return [np.asarray(data)[indicies] for data in data_list]


class Instrument(object):
    def __init__(self, start_time, N_det=64):
        self._detectors = [Detector(j) for j in range(N_det)]
        self._start = start_time
        # need to start counting from 0 after increment
        self._current_frame = -1
        self._current_index = None

    def add_new_frame(self, start_time, period, index):
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
        # list of start indicies for active and new frames
        condition = np.asarray(start_indicies) >= self._current_index
        frame_list, starts, p = filter_data([start_indicies,
                                             start_times,
                                             periods],
                                            condition)

        for k in range(len(frame_list)-1):
            current = frame_list[k]
            next_frame = frame_list[k + 1]
            self._add_data(self._current_frame,
                           IDs[current: next_frame],
                           all_times[current: next_frame],
                           all_amps[current: next_frame])
            self.add_new_frame(starts[k+1],
                               p[k+1],
                               frame_list[k+1])

        self._add_data(self._current_frame, IDs[self._current_index:],
                       all_times[frame_list[-1]:],
                       all_amps[frame_list[-1]:])

    def _add_data(self, frame, IDs, times, amps):
        for j, _ in enumerate(self._detectors):
            indicies = np.where(np.asarray(IDs) == j)[0]
            self._detectors[j].add_events_to_frame(frame,
                                                   np.asarray(times)[indicies],
                                                   np.asarray(amps)[indicies])
