import numpy as np
import time


def get_data():
    """
    Method to get the data for profiling.
    :return: the path, list of file names and number of detectors
    """
    path = ''
    name = [f'SIM0000000{k}' for k in range(1, 4)]
    # number of detectors
    N = 960
    return path, name, N


class Data(object):
    def __init__(self, x, marker, label):
        """
        Class to make it easier to handle data.
        :param x: the x values
        :param marker: the marker to use in plots
        :param label: the label for plots
        """
        self.x = x
        self.y = np.zeros(len(x))
        self.e = np.zeros(len(x))
        self.marker = marker
        self.label = label

    def add_data(self, index, y, e):
        """
        Adds y and error data to the
        index
        :param index: the index to add the data
        :param y: the y value
        :param e: the error value on y
        """
        self.y[index] = y
        self.e[index] = e

    def plot(self, ax):
        """
        Plots the data on the axis ax
        :param ax: the axis to plot on
        """
        ax.errorbar(self.x, self.y, self.e, fmt=self.marker, label=self.label)

    def plot_rate(self, ax, load):
        """
        Plots the rate, requires x to be events
        and y to be time.
        :param ax: the axis to add the plot to
        :param load: an array of the load times
        """
        rate = self.x/(load + self.y)
        ax.errorbar(self.x, rate, self.e/rate**2,
                    fmt=self.marker, label=self.label)


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
    filters = data.report_filters().time_filters.remove_filters.copy()
    if len(filters) > 0:
        for f in filters:
            data.delete_remove_data_time_between(f.name)
    return data


def get_stats(data, func, N_threads, N_stats):
    """
    Calculates the time taken to do histogram
    + filters on N_threads, it is then averaged
    over N_stats.
    :param data: the muon event data object
    :param func: the function for adding filters
    :param N_threads: the number of threads to use
    :param N_stats: the number of calculations to average
    :return: the mean and standard deviation of the time taken
    for the calculation.
    """
    tmp = np.zeros(N_stats)
    for k in range(N_stats):
        start = time.time()
        data = func(data)
        _ = data.histogram(N_threads=N_threads)
        tmp[k] = time.time() - start
        N = data._cache.get_N_events
        data = remove_filters(data)
    return np.mean(tmp), np.std(tmp), N
