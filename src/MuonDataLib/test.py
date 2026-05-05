import numpy as np
import h5py
#import time, dask.multiprocessing
#dask.config.set(scheduler = 'processes', num_workers = 4)

import numba
from numba import uint32, int32, float32, float64, int64
from numba import types
import numpy as np


from MuonDataLib.cython_ext.stats import add
#import MuonDataLib.cython_ext.event_data as ev
from numba.extending import get_cython_function_address as get_cython
addr = get_cython('MuonDataLib.cython_ext.stats', 'add')
import ctypes
#tmp = np.asarray([1, 2])

func_type = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(ctypes.c_int32))
moo = func_type(addr)

def get_max_threads():
    return numba.get_num_threads()

@numba.jit(float64[:](float64, float64, float64), nopython=True, fastmath=True, parallel=True)
def get_bin_edges(a_min, a_max, delta):
    bin_edges = np.zeros(int((a_max-a_min)/delta) + 1, dtype=np.float64)
    for i in numba.prange(bin_edges.shape[0]):
        bin_edges[i] = a_min + i * delta

    bin_edges[-1] = a_max  # Avoid roundoff error on last point
    return bin_edges


@numba.jit((float64[:], int32[:], int64, int32[:], int32[:], float64, float64, float64, float64, int32),
             fastmath=True, parallel=True)
def para_histogram(times, 
               spec,
               N_spec,
               periods,
               weight,
               min_time=0,
               max_time=30.,
               width=0.5,  
               conversion=1.e-3,
               N_threads=1):
    
    numba.set_num_threads(N_threads)
    bins = get_bin_edges(min_time, max_time, width)

    """
    lets make it possible to set the number of
    threads. Then can do a loop over number of
    threads to find optimum value
    """
    N = np.zeros(N_threads)
    result = np.zeros((N_threads, np.max(periods)+1, N_spec, len(bins)-1), dtype=np.int32)
    chunk = int(len(times)//N_threads)

    for thread in numba.prange(N_threads):
        # get slices
        start = thread*chunk
        stop = start + chunk
        if thread == N_threads-1:
            stop = len(times)
        for k in range(start, stop):
            time = times[k]*conversion
            if time <= max_time and time >= min_time:
                j_bin = int((time - min_time) // width)
                p = periods[k]
                det = spec[k]
                w = weight[k]
                result[thread, p, det, j_bin] += w
                N[thread] += w
        
    return np.sum(result, axis=0, dtype=np.int32), bins, np.sum(N)
