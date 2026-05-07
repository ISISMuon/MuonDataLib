from MuonDataLib.data.loader.load_events import load_events
from MuonDataLib.test import get_max_threads
from utils import add_N_filters, remove_filters, get_data, get_stats, Data
import matplotlib.pyplot as plt
import numpy as np
import os


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


class ThreadData(Data):
    def __init__(self, x, marker, label):
        super().__init__(x, marker, label)
        self.ref = np.zeros(len(x))
        self.ref_err = np.zeros(len(x))

    def add_data(self, index, y, e, ref, ref_err):
        super().add_data(index, y, e)
        self.ref[index] = ref
        self.ref_err[index] = ref_err

    def plot(self, ax):
        value = 100*self.y/(self.ref)
        error = value*np.sqrt((self.e/self.y)**2 + (self.ref_err/self.ref)**2)
        ax.errorbar(self.x, value, error, fmt=self.marker, label=self.label, capsize=6)
        #a#x.(self.x, value, label=self.label)

def no_filters(data):
    return data

def clear_filters(data):
    data = add_N_filters(data, 1)
    return remove_filters(data, 1)

def add_filters(data):
    return add_N_filters(data, N_filters)

def remove_all_filters(data):
    return remove_filters(data, N_filters)   


def get_result(para, para_err, seq, seq_err, N):
    values = 100*(para/seq)/N
    errors = 100*np.sqrt( (para_err/para)**2 + (seq_err/seq)**2)/N
    return values, errors

"""
Get speed of calculation for different file sizes
"""
thread_vals = np.arange(10, N_threads + 1)
stats = 20

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title(f'With filters (N={stats})')

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.set_title(f'Without filters (N={stats})')


for input_file in name:
    print(f'loading {input_file}')

    data = load_events(os.path.join(path, input_file + '.nxs'), N)
    
    seq, seq_e, _ = get_stats(data, add_filters, 0, stats)
    seq_0, seq_0_e, _ = get_stats(data, no_filters, 0, stats)

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
