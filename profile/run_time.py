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
stats = 2


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

seq_data = Data(np.zeros(len(name)), 'x', 'sequential')
para_data = Data(np.zeros(len(name)), 'x', 'parallel')

for k, input_file in enumerate(name):
    print(f'loading {input_file}')

    # get load times
    t0 = time.time()
    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    load[k] = time.time() - t0

    # get duration
    data.histogram()
    duration[k] = data._dict['raw_data']._cache.get_duration/(60.*60.)
    data = remove_filters(data)

    seq, seq_e, events = get_stats(data, add_filter, 1, stats)
    seq_data.add_data(k, seq, seq_e)

    para, para_e, events = get_stats(data, add_filter, N_threads, stats)
    para_data.add_data(k, para, para_e)

    N_events[k] = events
    del data

N_events = N_events/1.e6
para_data.x = N_events
seq_data.x = N_events

# plot events per second
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

para_data.plot_rate(ax1, load)
seq_data.plot_rate(ax1, load)

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
ax1.plot(N_events, load, 'kx', label='load')

ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Time (second)')
ax1.set_xlim([0, N_events[-1]*1.01])

ax2.set_xticks(N_events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()

plt.show()
