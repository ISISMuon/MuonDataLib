from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.numba.stats import get_max_threads
from utils import get_data, get_stats, Data
import matplotlib.pyplot as plt
import numpy as np
import os


"""
This script is for developer testing to check
the scaling of the histogram + filtering
for different size filters.
"""
N_threads = get_max_threads()
N_filters = 1

stats = 2
factor = np.asarray([0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 0.9])

print('Size of filter profile')

path, name, N = get_data()
N_events = np.zeros(len(factor))

for input_file in name[0:2]:
    print(f'loading {input_file}')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f'{input_file} (N={stats})')

    data = load_events(os.path.join(path, input_file + '.nxs'), N)

    # get first and last frame times
    tmp = data.get_frame_start_times()
    start = tmp[0]
    last = tmp[-1]

    seq_data = Data(factor, 'o', 'serial')
    para_data = Data(factor, 'x', 'parallel')

    for k, frac in enumerate(factor):
        print(f'{100*frac}%')

        def add_filter(data):
            """
            Need an add method that takes one
            argument, so define it here
            so it can use the value for frac.
            :param data: muon event data object
            :return: the muon event data object
            with a filter that covers frac of the
            data.
            """
            if frac == 0:
                return data
            stop = last*frac
            data.remove_data_time_between('filter',
                                          start,
                                          stop)
            return data

        para, para_e, _ = get_stats(data, add_filter, N_threads, stats)
        para_data.add_data(k, para, para_e)

        seq, seq_e, events = get_stats(data, add_filter, 1, stats)
        seq_data.add_data(k, seq, seq_e)

        N_events[k] = events

    para_data.plot(ax)
    seq_data.plot(ax)

    ax.set_ylabel('run time (s)')
    ax.set_xlabel('Fraction of data removed')
    ax.legend()
    ax.set_xlim([0, 1])

    ax2 = ax.twiny()
    ax2.set_xticks(para_data.x)
    ax2.set_xlabel('Millions of events')
    ax2.set_xticklabels([f'{n/1.e6:.1f}' for n in N_events])

    del data

plt.show()
