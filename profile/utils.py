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


class Data(object):

    def __init__(self, x, marker, label):
        self.x = x
        self.y = np.zeros(len(x))
        self.e = np.zeros(len(x))
        self.marker = marker
        self.label = label

    def add_data(self, index, y, e):
        self.y[index] = y
        self.e[index] = e

    def plot(self, ax):
        ax.errorbar(self.x, self.y, self.e, fmt=self.marker, label=self.label)

    def plot_rate(self, ax, load):
        rate = self.x/(load + self.y)
        ax.errorbar(self.x, rate, self.e/rate**2, fmt=self.marker, label=self.label)

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
 
def remove_filters(data):
    """
    A simple method to remove the filters.
    :param data: the MuonEventData object
    :return: the MuonEventData object
    """
    # this clears the cache for no filters
    data._clear()
    filters = data.report_filters()['time_filters']['remove_filters'].copy()
    if len(filters) > 0:
        for name in filters:
            data.delete_remove_data_time_between(name)
    return data


def get_data():
    # will need to update these to be the path and file names of your test data
    path = ''
    name = [f'SIM0000000{k}' for k in range(1, 3)]#7)]
    N = 960 #  number of detectors
    return name, N

def get_stats(data, func, N_threads, N_stats):
    tmp = np.zeros(N_stats)
    for k in range(N_stats):
        start = time.time()
        data = func(data)
        _ = data.histogram(N_threads=N_threads)
        tmp[k] = time.time() - start
        N = data._cache.get_N_events
        data = remove_filters(data)
    return np.mean(tmp), np.std(tmp), N
