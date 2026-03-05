from MuonDataLib.cython_ext.base_sample_logs import BaseSampleLogs
import numpy as np


def extract_event_data(inst, ID, frame):
    det = inst._detectors[ID]
    return det._frames[frame]


def get_sample_logs():
    logs = BaseSampleLogs()
    x_data = np.linspace(1, 4, 4)
    logs.add_sample_log('Temp', x_data, x_data*.1 - 2)
    logs.add_sample_log('B', x_data, x_data/2.)
    logs.add_sample_log('I', x_data, x_data)
    return logs
