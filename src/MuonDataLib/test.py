import pandas as pd
import numpy as np

import dask.dataframe as dd
import dask.array as da

#import time, dask.multiprocessing
#dask.config.set(scheduler = 'processes', num_workers = 4)

import numba
from numba import uint32, int32, float32, float64, int64
from numba import types
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

def para_histogram(times, 
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


#@numba.jit((float64[:], int32[:], int64, int32[:], int32[:], float64[:], float64, float64, float64, float64),
@numba.jit((float64[:], int32[:], int64, int32[:], int32[:], float64[:], float64, float64, float64, float64),
           parallel=True, fastmath=True)
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


string = types.unicode_type

@numba.jit()#int32(float64[:], int64, int64, float64))
def _binary_search(
                    values,
                    start,
                    stop,
                    target):

    """
    A simple recursive binary search. The expectation is that
    values are sorted into ascending order. It returns the
    index of the left bounding bin for the target value.

    :param values: The list of ordered time values to search against
    :param start: The lowest index to include in the search
    :param stop: The largest index to include in the search
    :param target: The value we want to search for
    :returns: The index of the left bounding bin of the target
    """
    if stop - start == 1:
        return start

    elif stop > start:
        mid_point = start + (stop - start) //2

        if values[mid_point] == target:
            return mid_point

        elif values[mid_point] > target:
            return _binary_search(values, start, mid_point, target)

        else:
            return _binary_search(values, mid_point, stop, target)
    elif values[start] < target or values[stop] > target:
        return -1
    else:
        return stop


#from MuonDataLib.cython_ext.utils import binary_search
@numba.jit(int32(float64[:], int64, int64, float64, string, string))
def binary_search(  values,
                    start,
                    stop,
                    target,
                    name='value',
                    unit=''):

    """
    A simple recursive binary search. The expectation is that
    values are sorted into ascending order. It returns the
    index of the left bounding bin for the target value.

    This method adds a simple check before the main calculation.
    :param values: The list of ordered time values to search against
    :param start: The lowest index to include in the search
    :param stop: The largest index to include in the search
    :param target: The value we want to search for
    :returns: The index of the left bounding bin of the target
    """
    if values[0] > target:
        
        print(f'The target {target} is before the first {name} {values[0]} {unit}. Difference is {values[0]-target} {unit}')


    elif values[len(values)-1] < target:
        i = len(values) - 1
        print(f'The target {target} is after the last {name} {values[i]} {unit}. Difference is {target-values[i]} {unit}')


    return _binary_search(values, start, stop, target)

@numba.jit((float64[:], float64[:], float64[:], types.unicode_type, types.unicode_type), parallel=True)
def get_p_indices(times, f_start, f_end,
                  name='value', unit=''):
    """
    Method for calculating which frames filters belong to.
    This assumes that all data is in order.
    It uses a binary search to find the index of the left bound of the bin
    containing the desired value. Since the filter times are in order
    the next search can have a start value of equal to the index found for
    the previous filter. Similarly the first end filter must be after the
    start for the first filter.


    :param times: the list of frame start times
    :param f_start: a list of filter start times
    :param f_end: a list of filter end times
    :param name: the name of the thing we are filtering on
    :param unit: the unit of the thing being filtered
    :result: the list of start and end frame indices for the filters
    """
    N = len(f_start)
    M = len(times)
    j_start = np.zeros(N, dtype=np.int32)
    j_end = np.zeros(N, dtype=np.int32)
    start = 0

    for j in range(N):
        j_start[j] = binary_search(times, start, M, f_start[j], name, unit)
        start = j_start[j]

    # the first end filter must be after the first start filter
    start = j_start[0]
    for j in range(N):
        j_end[j] = binary_search(times, start, M, f_end[j], name, unit)

    return j_start, j_end

