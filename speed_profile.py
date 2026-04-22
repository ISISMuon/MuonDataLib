from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.data.utils import convert_date
import datetime
import os
import sys

import datetime
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import h5py
from MuonDataLib.cython_ext.load_events import load_data, _load_data
from MuonDataLib.test import p_load, n_load

def add_N_filters(data, N):
    frames = data.get_frame_start_times()
    m = 0
    c = 0
    for j in range(len(frames)-1):
        width = frames[j+1] - frames[j]
        if width > 0 and c ==0:
            data.remove_data_time_between(f'mo_{m}',
                                          frames[j] + 0.2*width,
                                          frames[j] + 0.8*width)
            c += 1
            m += 1
        elif m == N:
            return data
        else:
           c = 0
 
def remove_filters(data, N):

    for j in range(N):
        data.delete_remove_data_time_between(f'mo_{j}')
    return data


print('start speed profile')   
tmp = []
para = []
events = []
duration = []

# will need to update these to be the path and file names of your test data
path = ''
name = [f'SIM0000000{k}' for k in range(1, 7)]
#name = ['SIM00000001', 'SIM00000005']
N = 960 #  number of detectors
N_filters = 1


for input_file in name:
    print(f'loading {input_file}')
    
    start = time.time()
    _ = _load_data(input_file + '.nxs')
    tmp.append(time.time() - start)

    start = time.time()
    _ = p_load(input_file + '.nxs')
    para.append(time.time() - start)

    start = time.time()
    c = n_load(input_file + '.nxs')
    b = time.time() - start
    print(c[0])
    print(tmp[-1], para[-1], b)
    """
    # get load times
    t0 = time.time()
    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    load = time.time() - t0


    t0 = time.time()
    data = add_N_filters(data, N_filters)
    a, b = data.histogram()
    tmp.append(time.time() - t0 + load)
    events.append(data._events.get_N_events)
    duration.append(data._dict['raw_data']._cache.get_duration/(60.*60.)) # convert from sec to hours

    # remove the filter to clear the cache
    data = remove_filters(data, N_filters) 

    # add the filter back

    t0 = time.time()
    data = add_N_filters(data, N_filters)
    c, d = data.histogram(parallel=True)
    para.append(time.time() - t0 + load)
    
    print('duration', duration[-1])
    print('time', tmp[-1], para[-1])
    print("event check", events[-1], events[-1] - data._events.get_N_events)
    print('det check', len(a[0]), len(c[0]))
    del data


# for this part the user will need to install matplotlib
from MuonDataLib.plot.basic import Figure
import matplotlib.pyplot as plt
import numpy as np

events = np.asarray(events)/1.e6
duration = np.asarray(duration)
tmp = np.asarray(tmp)
para = np.asarray(para)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(events, events/(tmp), 'o', label='serial')
ax1.plot(events, events/(para), 'o', label='parallel')
ax1.set_xlabel('Millions of events')
ax1.set_ylabel('Millions of events per second')
ax1.set_xlim([0, events[-1]*1.01])

ax2.set_xticks(events)
ax2.set_xticklabels([f'{d:.1f}' for d in duration])
ax2.set_xlabel('Duration (hours)')


ax1.legend()
plt.show()
"""
