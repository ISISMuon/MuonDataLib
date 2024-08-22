from MuonDataLib.cython_ext.event_data import Events
from MuonDataLib.cython_ext.filters.filter_manager import FilterManager

import h5py
import numpy as np
import time
cimport numpy as cnp
import cython
cnp.import_array()


def _load_data(file_name):
        """
        Loads event data from the event nxs file.
        This should make it easier to swap out later.
        :param file_name: the name of the file to load.
        :return: IDs, first index for frame, time stamps,
        amplitudes, time at the start of the frame
        """

        with h5py.File(file_name, 'r') as file:
            tmp = file.require_group('raw_data_1')
            tmp = tmp.require_group('detector_1')

            N = tmp['event_id'].len()

            IDs = np.zeros(N, dtype=np.int32)
            times = np.zeros(N, dtype=np.double)
            amps = np.zeros(N, dtype=np.double)

            M = tmp['event_index'].len()
            start_j = np.zeros(M, dtype=np.int32)
            start_t = np.zeros(M, dtype=np.double)

            tmp['event_id'].read_direct(IDs)
            tmp['event_time_offset'].read_direct(times)
            tmp['pulse_height'].read_direct(amps)
            tmp['event_index'].read_direct(start_j)
            tmp['event_time_zero'].read_direct(start_t)

        return IDs, start_j, times, amps, start_t

def load_data(file_name):
        """
        Loads the data from an event nxs file
        :param file_name: the name of the event nxs file to load
        :return: the time to run this method, the events object, a filter object
        """
        start = time.time()
        IDs, frames, times, amps, frame_times = _load_data(file_name)
        events = Events(IDs, times)
        filters = FilterManager(frames, frame_times, len(IDs))
        filters.create_min_filter('amplitude', amps)
        return time.time() - start, events, filters


