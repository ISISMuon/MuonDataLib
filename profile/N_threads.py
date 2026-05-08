from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.numba.stats import get_max_threads
from utils import add_N_filters, get_data, get_stats, Data
import matplotlib.pyplot as plt
import numpy as np
import os


"""
This script is for developer testing to check
the scaling of the histogram + filtering
for different number of threads.
"""
N_threads = get_max_threads()
N_filters = 1
stats = 2
thread_vals = np.arange(1, N_threads + 1)


class ThreadData(Data):
    def __init__(self, x, marker, label):
        """
        A wraper on the Data class to make
        it easier to do percentage of the
        original speed.
        :param x: x values (number threads)
        :param marker: the marker value for the plot
        :param label: the label for the plot
        """
        super().__init__(x, marker, label)
        self.ref = np.zeros(len(x))
        self.ref_err = np.zeros(len(x))

    def add_data(self, index, y, e, ref, ref_err):
        """
        Adds data to the class
        :param index: the array index of the data
        :param y: the y value (run time)
        :param e: the error on y
        :param ref: the reference value (run time for serial)
        :param ref_err: the error on reference value
        """
        super().add_data(index, y, e)
        self.ref[index] = ref
        self.ref_err[index] = ref_err

    def plot(self, ax):
        """
        Plot the percentage relative to the serial speed
        :param ax: the axis to plot to
        """
        value = 100*self.y/(self.ref)
        error = value*np.sqrt((self.e/self.y)**2
                              + (self.ref_err/self.ref)**2)
        ax.errorbar(self.x, value, error,
                    fmt=self.marker, label=self.label, capsize=6)


def no_filters(data):
    """
    Do nothing
    :param data: the muon event data
    :return: the muon event data
    """
    return data


def add_filters(data):
    """
    A wrapper for adding N filters
    :param data: the muon event data
    :return: the muon event data
    """
    return add_N_filters(data, N_filters)


print('Number of threads profile')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title(f'With filters (N={stats})')

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_title(f'Without filters (N={stats})')

path, name, N = get_data()

for input_file in name:
    print(f'loading {input_file}')

    data = load_events(os.path.join(path, input_file + '.nxs'), N)

    seq, seq_e, _ = get_stats(data, add_filters, 1, stats)
    seq_0, seq_0_e, _ = get_stats(data, no_filters, 1, stats)

    filters = ThreadData(thread_vals, 'o', f'{input_file}, 100% = {seq:.2f} s')
    none = ThreadData(thread_vals, 'x', f'{input_file}, 100% = {seq_0:.2f} s')

    for k, threads in enumerate(thread_vals):
        print(f'{threads} of {N_threads}')

        para, para_e, _ = get_stats(data, add_filters, threads, stats)
        filters.add_data(k, para, para_e, seq, seq_e)

        para, para_e, _ = get_stats(data, no_filters, threads, stats)
        none.add_data(k, para, para_e, seq_0, seq_0_e)

    print()
    filters.plot(ax)
    none.plot(ax2)

    del data

for axis in [ax, ax2]:
    axis.set_ylabel('Percentage time for parallel wrt sequential')
    axis.set_xlabel('Number of threads')
    axis.plot(thread_vals, 100*np.ones(len(thread_vals)), 'k--')
    axis.legend()

plt.show()
print()
