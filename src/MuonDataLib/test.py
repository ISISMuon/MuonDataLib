import pandas as pd
import numpy as np

import dask.dataframe as dd
import dask.array as da

#import time, dask.multiprocessing
#dask.config.set(scheduler = 'processes', num_workers = 4)

import numba
from numba import uint32, int32, float32, float64, int64
import numpy as np


@numba.jit(float64[:](float64, float64, float64), nopython=True, fastmath=True, parallel=True)
def get_bin_edges(a_min, a_max, delta):
    bin_edges = np.zeros(int((a_max-a_min)/delta), dtype=np.float64)
    for i in numba.prange(bin_edges.shape[0]):
        bin_edges[i] = a_min + i * delta

    bin_edges[-1] = a_max  # Avoid roundoff error on last point
    return bin_edges


def make_numba(times, 
               spec,
               N_spec,
               periods,
               weight,
               min_time=0,
               max_time=30.,
               width=0.5,
               conversion=1.e-3):

    bins = get_bin_edges(min_time, max_time, width)
    result, N = do_stuff(times, 
                      spec,
                      N_spec, 
                      periods,
                      weight, 
                      bins, min_time, max_time, width, conversion)
    return result, bins, N

#@numba.jit((float64[:], int32[:], int64, int32[:], int32[:], float64[:], float64, float64, float64, float64),
@numba.jit((float64[:], uint32[:], int64, int32[:], int32[:], float64[:], float64, float64, float64, float64),
           parallel=True)
def do_stuff(
             times,
             spec,
             N_spec,
             periods,
             weight,
             bins,
             min_time=0,
             max_time=30.,
             width=0.5,
             conversion=1.e-3):
    N = 0
    result = np.zeros((np.max(periods)+1, N_spec, len(bins)-1), dtype=np.int32)
    for k in numba.prange(len(times)):
        det = spec[k]
        time = times[k] * conversion
        if time <= max_time and time >= min_time:
            p = periods[k]
            j_bin = int((time - min_time) // width)
            w_k = 1*weight[k]
            result[p, det, j_bin] += w_k
            N += w_k
    return result, N        


def make_hist(times, 
              spec,
              N_spec,
              periods,
              weight,
              min_time=0,
              max_time=30.,
              width=0.5,
              conversion=1.e-3):

    bins = np.arange(min_time, max_time + width, width, dtype=np.double)
    
    df = pd.DataFrame({'id':np.array(spec), 
                       'periods': np.array(periods),
                       'times':np.array(times)*conversion})
    result = np.zeros((np.max(periods)+1, N_spec, len(bins)-1), dtype=np.int32)
    
    for p in range(np.max(periods)+1):
        for i in range(N_spec):
            a = df.loc[(df['id']==i) & (df['periods']==p),
                       ['times']]#.T.iloc[0].value_counts(bins=bins, sort=False)
            #print(p, i, N_spec, np.max(periods), a)
            if not a.empty:
                result[p, i, :] = a.T.iloc[0].value_counts(bins=bins, sort=False)
    return result, bins, np.sum(result)

def make_numba2(times, 
               spec,
               N_spec,
               periods,
               weight,
               min_time=0,
               max_time=30.,
               width=0.5,
               conversion=1.e-3):

    bins = get_bin_edges(min_time, max_time, width)
    result, N = do_stuff2(times, 
                          spec,
                          N_spec, 
                          periods,
                          weight, 
                          bins,
                          min_time,
                          max_time,
                          width,
                          conversion
                          )
    return result, bins, N


@numba.jit((float64[:], int32[:], int64, int32[:], int32[:], float64[:], float64, float64, float64, float64),
           parallel=True)
def do_stuff2(
             times,
             spec,
             N_spec,
             periods,
             weight,
             bins,
             min_time=0,
             max_time=30.,
             width=0.5,
             conversion=1.e-3
             ):
    N = 0
    result = np.zeros((np.max(periods)+1, N_spec, len(bins)-1), dtype=np.int32)
    for k in numba.prange(len(times)):
        det = spec[k]
        time = times[k] * conversion
        if time <= max_time and time >= min_time:
            p = periods[k]
            j_bin = int((time - min_time) // width)
            w_k = 1*weight[k]
            result[p, det, j_bin] += w_k
            N += w_k
 
    return result, N        
