from MuonDataLib.data.events.instrument import Instrument
import h5py
import numpy as np


class LoadEventData(object):
    def __init__(self):
        self._bin_width = 0.5
        self._inst = None
        self._file_name = None

    def set_bin_width(self, width):
        self._bin_width = width

    def reload_data(self):
        with h5py.File(self._file_name, 'r') as file:
            tmp = file.require_group('raw_data_1')
            tmp = tmp.require_group('detector_1')
            IDs = tmp['event_id'][:]
            start_indicies = tmp['event_index'][:]
            times = tmp['event_time_offset'][:]
            start_times = tmp['event_time_zero'][:]
            periods = tmp['period_number'][:]
            amps = tmp['pulse_height'][:]
            # add data
            self._inst.add_event_data(IDs,
                                      times,
                                      amps,
                                      periods,
                                      start_times,
                                      start_indicies)

    def load_data(self, file_name):
        self._file_name = file_name
        with h5py.File(self._file_name, 'r') as file:
            tmp = file.require_group('raw_data_1')
            tmp = tmp.require_group('detector_1')
            IDs = tmp['event_id'][:]
            start_indicies = tmp['event_index'][:]
            times = tmp['event_time_offset'][:]
            start_times = tmp['event_time_zero'][:]
            periods = tmp['period_number'][:]
            amps = tmp['pulse_height'][:]
            # start is attribute from event_time_zero?
            start = tmp['event_time_zero'].attrs['offset'][0]

            self._inst = Instrument(start, np.max(IDs))
            # add frame
            self._inst.add_new_frame(start_times[0],
                                     periods[0],
                                     start_indicies[0])
            # add data
            self._inst.add_event_data(IDs,
                                      times,
                                      amps,
                                      periods,
                                      start_times,
                                      start_indicies)
