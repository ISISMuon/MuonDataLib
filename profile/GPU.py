from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.numba.stats import get_max_threads
import os
import numpy as np
from utils import add_N_filters, remove_filters, get_data, Data, get_stats
import matplotlib.pyplot as plt
import time


"""
This script is for developer testing to check
the scaling of the histogram + filtering
for different number of threads.
"""
N_threads = get_max_threads()
stats = 6

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




def add_filter(data):
    """
    wrapper for add_N_filters
    :param data: the muon event data
    :return: the muon event data with fitlers
    """
    return add_N_filters(data, 1)


print('start speed profile')

path, name, N = get_data()

duration = np.zeros(len(name))
N_events = np.zeros(len(name))
load = np.zeros(len(name))

seq_data = Data(np.zeros(len(name)), 'x', 'serial')
para_data = Data(np.zeros(len(name)), 'x', 'parallel')
gpu_data = Data(np.zeros(len(name)), 'x', 'GPU')

cf_cpu_data = ThreadData(np.zeros(len(name)), 'x', 'parallel')
cf_gpu_data = ThreadData(np.zeros(len(name)), 'x', 'GPU')

"""
a, b, c = np.load('none.npy')
no_data.x = a
no_data.y = b
no_data.e = c

a, b, c = np.load('filter.npy')
old_data.x = a
old_data.y = b
old_data.e = c
"""
for k, input_file in enumerate(name):
    print(f'loading {input_file}')

    # get load times
    t0 = time.time()
    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    load[k] = time.time() - t0
    print('load time', load[k])
    # get duration
    data.histogram(N_threads=0)
    duration[k] = data._dict['raw_data']._cache.get_duration/(60.*60.)
    data = remove_filters(data)

    seq, seq_e, events = get_stats(data, add_filter, 1, stats)
    seq_data.add_data(k, seq, seq_e)

    gpu, gpu_e, events = get_stats(data, add_filter, 0, stats)
    gpu_data.add_data(k, gpu, gpu_e)
    cf_gpu_data.add_data(k, gpu, gpu_e, seq, seq_e)


    para, para_e, events = get_stats(data, add_filter, N_threads, stats)
    para_data.add_data(k, para, para_e)
    cf_cpu_data.add_data(k, para, para_e, seq, seq_e)

    N_events[k] = events
    del data

N_events = N_events/1.e6
para_data.x = N_events
seq_data.x = N_events
gpu_data.x = N_events
cf_gpu_data.x = N_events
cf_cpu_data.x = N_events

# plot events per second
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

seq_data.plot_rate(ax1, load)
para_data.plot_rate(ax1, load)
gpu_data.plot_rate(ax1, load)
#old_data.plot_rate(ax1, load)
#no_data.plot_rate(ax1, load)

ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Millions of events per second')
ax1.set_xlim([0, N_events[-1]*1.01])

ax2.set_xticks(N_events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()

# plot just run times
figb = plt.figure()
ax1 = figb.add_subplot(111)
ax2 = ax1.twiny()

seq_data.plot(ax1)
para_data.plot(ax1)
gpu_data.plot(ax1)
#old_data.plot(ax1)
#no_data.plot(ax1)
#  ax1.plot(N_events, load, 'kx', label='load')

ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Time (second)')
ax1.set_xlim([0, N_events[-1]*1.01])

ax2.set_xticks(N_events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()

# plot percentage speed up
figc = plt.figure()
ax1 = figc.add_subplot(111)
ax2 = ax1.twiny()

cf_cpu_data.plot(ax1)
cf_gpu_data.plot(ax1)
ax1.plot(N_events, np.ones(len(N_events))*100, 'k--')
ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Percentage time wrt to serial')
ax1.set_xlim([0, N_events[-1]*1.01])

ax2.set_xticks(N_events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()

plt.show()
