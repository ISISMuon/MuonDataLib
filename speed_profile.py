from MuonDataLib.data.loader.load_events import load_events
import os
import sys

import datetime
import numpy as np
import matplotlib.pyplot as plt
import time

print('go')   

#a = np.asarray([1, 2, 1.2, 1.3, 1.2, 1.4, 1.5])
#print(np.where(a > 1.3, a, 0))
path = os.path.join('..', 'cpp_test', 'fast_python_test')
tmp = []
para = []
events = []

name = ['HIFI00194953', 'HIFI00193572', 'HIFI00194374', 'HIFI00196869', 'HIFI00195570', 'HIFI00005873']


path = ''
name = [f'SIM0000000{k}' for k in range(1, 7)]

#data = load_events(os.path.join(path, name[0] + '.nxs'), 64)

for input_file in name:
    print(input_file)
    # get load times
    t0 = time.time()
    data = load_events(os.path.join(path, input_file + '.nxs'), 960)
    data.remove_data_time_between('mo', 1., 1.2)
    load = 0#time.time() - t0

    t0 = time.time()
    a, b = data.histogram()
    tmp.append(time.time() - t0 + load)
    events.append(data._events.get_N_events)
    
    data.delete_remove_data_time_between('mo')

    data.remove_data_time_between('mo', 1., 1.2)
    t0 = time.time()
    c, d = data.histogram(parallel=True)
    para.append(time.time() - t0 + load)
    print('time', tmp[-1], para[-1])
    print("event check", events[-1] - data._events.get_N_events)
    print('det check', len(a[0]), len(c[0]))
    del data


from MuonDataLib.plot.basic import Figure
import matplotlib.pyplot as plt
import numpy as np

#sizes = [4.6, 2.4, 3.6, 5.0, 5.9, 4.2]

fig = plt.figure()
events = np.asarray(events)/1.e6
tmp = np.asarray(tmp)
para = np.asarray(para)

plt.plot(events, events/(tmp), 'o', label='serial')
plt.plot(events, events/(para), 'o', label='parallel')
plt.xlabel('Millions of events')
plt.ylabel('Millions of events per second')

#plt.plot(sizes, mantid_load, 'x', label='Mantid load')
#plt.plot(sizes, mantid_hist, '*', label='Mantid hist')
#plt.plot(sizes, mantid_load + mantid_hist, 'o', label='Mantid total')

plt.legend()
plt.show()

