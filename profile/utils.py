from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.data.utils import convert_date
import datetime
import os
import sys

import datetime
import numpy as np
import matplotlib.pyplot as plt
import time
from MuonDataLib.cython_ext.load_events import load_data, _load_data

"""
Lets split these up:
    - 1 filter for N files
    - N filters for 1 file
    - filter of size N for 2 files (big and small)
where N is the quantity being looped over
"""



def add_N_filters(data, N):
    """
    Simple method for adding N filters,
    they are placed every other frame.
    This maximises the computational expense
    of the calculation.
    :param data: the MuonEventData object
    :param N: the number of filters
    :return: the updated MuonEventData object
    """
    if N == 0:
        return data
    frames = data.get_frame_start_times()
    offset = frames[100]
    m = 0
    skip = False
    for j in range(len(frames)-1):
        width = frames[j+1] - frames[j]
        if width > 0 and not skip:
            data.remove_data_time_between(f'tmp_{m}',
                                          offset*(j+1) + frames[j] + .2*width,
                                          offset*(j+1) + frames[j] + 7.8*width)
            skip = True
            m += 1
        elif m == N:
            return data
        else:
           skip = False
 
def remove_filters(data, N):
    """
    A simple method to remove the filters.
    :param data: the MuonEventData object
    :param N: the number of filters to remove
    :return: the MuonEventData object
    """
    if N == 0:
        return data
    for j in range(N):
        data.delete_remove_data_time_between(f'tmp_{j}')
    return data


def get_data():
    # will need to update these to be the path and file names of your test data
    path = ''
    name = [f'SIM0000000{k}' for k in range(1, 7)]
    N = 960 #  number of detectors
    return name, N
