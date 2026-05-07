from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.test import get_max_threads
from utils import add_N_filters, remove_filters, get_data, get_stats, Data
import matplotlib.pyplot as plt
import numpy as np
import os


print('Size of filter profile')   

# will need to update these to be the path and file names of your test data
path = ''
name, N = get_data()
N_threads = get_max_threads()
N_filters = 1

stats = 20

factor = np.asarray([0, 0.1, 0.25, 0.5, 0.75, 0.9])

for input_file in name[0:2]:
    print(f'loading {input_file}')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f'{input_file} (N={stats})')


    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    
    tmp = data.get_frame_start_times()
    start = tmp[0]
    last = tmp[-1]
    seq_data = Data(factor, 'o', 'serial')
    para_data = Data(factor, 'x', 'parallel') 


    for k, frac in enumerate(factor):
        print(f'{100*frac}%')
        def add_filter(data):
           if frac==0:
               return data
           stop = last*frac
           data.remove_data_time_between('filter',
                                         start,
                                         stop)
           return data

        """
        want to change stats to get the N_events
        """
        para, para_e, _ = get_stats(data, add_filter, N_threads, stats)
        para_data.add_data(k, para, para_e)

        seq, seq_e, _ = get_stats(data, add_filter, 0, stats)
        seq_data.add_data(k, seq, seq_e)

        

    para_data.plot(ax)
    seq_data.plot(ax)
    ax.set_ylabel('run time (s)')
    ax.set_xlabel('Fraction of data removed')
    ax.legend()
    del data

plt.show()
