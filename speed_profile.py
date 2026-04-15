from MuonDataLib.data.loader.load_events import load_events
import os
import sys

import datetime
import numpy as np
import matplotlib.pyplot as plt
import time

print('start speed profile')   
tmp = []
para = []
events = []


# will need to update these to be the path and file names of your test data
path = ''
name = [f'SIM0000000{k}' for k in range(1, 7)]
name = ['SIM00000001', 'SIM00000006']
N = 960 #  number of detectors


for input_file in name:
    print(f'loading {input_file}')
    # get load times
    t0 = time.time()
    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    data.remove_data_time_between('mo', 1., 1.2)
    load = 0 #  time.time() - t0

    t0 = time.time()
    a, b = data.histogram()
    tmp.append(time.time() - t0 + load)
    events.append(data._events.get_N_events)
    
    # remove the filter to clear the cache
    data.delete_remove_data_time_between('mo')

    # add the filter back
    data.remove_data_time_between('mo', 1., 1.2)

    t0 = time.time()
    c, d = data.histogram(parallel=True)
    para.append(time.time() - t0 + load)
    
    print('time', tmp[-1], para[-1])
    print("event check", events[-1] - data._events.get_N_events)
    print('det check', len(a[0]), len(c[0]))
    del data

# for this part the user will need to install matplotlib
from MuonDataLib.plot.basic import Figure
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
events = np.asarray(events)/1.e6
tmp = np.asarray(tmp)
para = np.asarray(para)

plt.plot(events, events/(tmp), 'o', label='serial')
plt.plot(events, events/(para), 'o', label='parallel')
plt.xlabel('Millions of events')
plt.ylabel('Millions of events per second')

plt.legend()
plt.show()

