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


print('start speed profile')   
seq= []
para = []
seq_0 = []
para_0 = []
load = []
events = []
duration = []

# will need to update these to be the path and file names of your test data
path = ''
name = [f'SIM0000000{k}' for k in range(1, 7)]
N = 960 #  number of detectors
N_filters = 1

"""
Get speed of calculation for different file sizes
"""
for input_file in name:
    print(f'loading {input_file}')

    # get load times
    t0 = time.time()
    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    load.append(time.time() - t0)
    
    # get the number of events in the file and duration
    start = time.time()
    a, b = data.histogram()
    seq_0.append(time.time() - start)
    events.append(data._cache.get_N_events)
    # convert from sec to hours
    duration.append(data._dict['raw_data']._cache.get_duration/(60.*60.))



    # get the non-parallel times
    t0 = time.time()
    data = add_N_filters(data, N_filters)
    a, b = data.histogram()
    seq.append(time.time() - t0)

    # remove the filter to clear the cache
    data = remove_filters(data, N_filters) 

    # add the filter back
    t0 = time.time()
    data = add_N_filters(data, N_filters)
    c, d = data.histogram(parallel=True)
    para.append(time.time() - t0)
 
    # remove the filter to clear the cache
    data = remove_filters(data, N_filters) 
    t0 = time.time()
    c, d = data.histogram(parallel=True)
    para_0.append(time.time() - t0)
 
   
    print('duration', duration[-1])
    print('time with', seq[-1], para[-1])
    print('time', seq_0[-1], para_0[-1])
    print("event check", events[-1], events[-1] - data._events.get_N_events)
    print('det check', len(a[0]), len(c[0]))
    del data

"""
Get speed of calculation for different number of filters
"""
N_seq = []
N_para = []
N_events = []

filters = [0, 1]#, 5, 10, 15, 20, 50, 100, 150, 200]

data = load_events(os.path.join(path, name[-1] + '.nxs'), N)
for M in filters:
    print(f'loading {input_file} with {M} filters')

 
    # get the non-parallel times
    t0 = time.time()
    data = add_N_filters(data, M)
    a, b = data.histogram()
    N_seq.append(time.time() - t0)
    N_events.append(data._cache.get_N_events)

    # remove the filter to clear the cache
    data = remove_filters(data, M) 
    data._cache.clear()
    # add the filter back
    t0 = time.time()
    data = add_N_filters(data, M)
    c, d = data.histogram(parallel=True)
    N_para.append(time.time() - t0)
    print('N events', data._cache.get_N_events, np.sum(c), np.sum(a))

    print('time',N_events, N_seq[-1], N_para[-1])
    # remove the filter to clear the cache
    data = remove_filters(data, M) 
    data._cache.clear()

print()
"""
This is a development tool, so not expected to
be used by typical users. To run the following
you will need to install matplotlib
"""
from MuonDataLib.plot.basic import Figure
import matplotlib.pyplot as plt
import numpy as np

events = np.asarray(events)/1.e6
duration = np.asarray(duration)
load = np.asarray(load)
para = np.asarray(para)
seq = np.asarray(seq)
para_0 = np.asarray(para_0)
seq_0 = np.asarray(seq_0)

N_seq = np.asarray(N_seq)
N_para = np.asarray(N_para)
N_events = np.asarray(N_events)

# plot events per second
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(events, events/(seq + load), 'o', label='serial')
ax1.plot(events, events/(seq_0 + load), 'x', label='serial (no filter)')
ax1.plot(events, events/(para + load), 'o', label='parallel')
ax1.plot(events, events/(para_0 + load), 'x', label='parallel (no filter)')
ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Millions of events per second')
ax1.set_xlim([0, events[-1]*1.01])

ax2.set_xticks(events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()

# plot just run times
figb = plt.figure()
ax1 = figb.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(events, seq, 'o', label='serial')
ax1.plot(events, seq_0, 'x', label='serial (no filter)')
ax1.plot(events, para, 'o', label='parallel')
ax1.plot(events, para_0, 'x', label='parallel (no filter)')
ax1.plot(events, load, 'o', label='load')
ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Time (second)')
ax1.set_xlim([0, events[-1]*1.01])

ax2.set_xticks(events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()

# plot histogram times, these are from print to screen using desktop

serial_ = [0.34, 0.35, 2.31, 5.01, 7.28, 32.56]
parallel_ = [0.11, .28, 1.54, 3.18, 4.85, 9.66]


figc = plt.figure()
ax1 = figc.add_subplot(111)
ax2 = ax1.twiny()
ax1.plot(events, serial_, label='serial')
ax1.plot(events, parallel_, label='parallel')
ax1.set_ylabel('Time (seconds)')
ax1.set_xlabel('Millions of Events')
#ax1.set_xlim([N_events[0]*0.99, N_events[-1]*1.01])

ax2.set_xticks(events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')

ax1.legend()


plt.show()
