from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.data.utils import convert_date
from MuonDataLib.test import get_max_threads
import datetime
import os
import sys
from utils import add_N_filters, remove_filters, get_data
import matplotlib.pyplot as plt
import time
from MuonDataLib.cython_ext.load_events import load_data, _load_data
from MuonDataLib.plot.basic import Figure
import matplotlib.pyplot as plt
import numpy as np


"""
Lets split these up:
    - 1 filter for N files
    - N filters for 1 file
    - filter of size N for 2 files (big and small)
where N is the quantity being looped over
"""


print('Number of threads profile')   

# will need to update these to be the path and file names of your test data
path = ''
name, N = get_data()
N_threads = get_max_threads()
N_filters = 1

"""
Get speed of calculation for different file sizes
"""

for input_file in name:
    print(f'loading {input_file}')

    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    events = 0
    seq = []
    para = []
    seq_0 = []
    para_0 = []
    x_axis = []

    for threads in range(1, N_threads + 1):
    
        # get the number of events in the file and duration
        start = time.time()
        a, b = data.histogram(N_threads=0)
        seq_0.append(time.time() - start)
        events = data._cache.get_N_events
  
        # get the non-parallel times
        t0 = time.time()
        data = add_N_filters(data, N_filters)
        a, b = data.histogram(N_threads=0)
        seq.append(time.time() - t0)
    
        # remove the filter to clear the cache
        data = remove_filters(data, N_filters) 
  
        t0 = time.time()
        c, d = data.histogram(N_threads=threads)
        para_0.append(time.time() - t0)
    
        # add the filter back
        t0 = time.time()
        data = add_N_filters(data, N_filters)
        c, d = data.histogram(N_threads=threads)
        para.append(time.time() - t0)
         
        # remove the filter to clear the cache
        data = remove_filters(data, N_filters)   
     
        print('time with', seq[-1], para[-1])
        print('time', seq_0[-1], para_0[-1])

    threads = np.arange(1, N_threads+1)
    seq = np.asarray(seq)
    seq_0 = np.asarray(seq_0)
    para = np.asarray(para)
    para_0 = np.asarray(para_0)
    
    plt.plot(threads, para - seq, label=f'{input_file} with filters')
    plt.plot(threads, para_0 - seq_0, label=f'{input_file} without filters')
    
    del data

plt.plot(threads, np.zeros(len(threads)), 'k--')
plt.ylabel('parallel time - sequential time (s)')
plt.xlabel('Number of threads')
plt.legend()
plt.show()
 
print()
