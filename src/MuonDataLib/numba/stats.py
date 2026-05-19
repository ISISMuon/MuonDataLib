import numpy as np

import numba
from numba import int32, float64, int64


def get_max_threads():
    """
    Gets the max number of threads that
    numba will use
    :return: the number of threads to be used
    """
    return numba.get_num_threads()


@numba.jit(float64[:](float64, float64, float64),
           nopython=True, fastmath=True, parallel=True)
def get_bin_edges(a_min, a_max, width):
    """
    A method to caclculate histogram bin edges,
    given the range and bin width.
    :param a_min: the first bin edge
    :param a_max: the last bin edge
    :param width: the bin width
    :return: the bin edges
    """
    bin_edges = np.zeros(int((a_max-a_min)/width) + 1, dtype=np.float64)
    for i in numba.prange(bin_edges.shape[0]):
        bin_edges[i] = a_min + i * width

    bin_edges[-1] = a_max  # Avoid roundoff error on last point
    return bin_edges


@numba.jit((float64[:], int32[:], int64, int32[:],
            int32, int32[:], float64, float64, float64,
            float64, int64), fastmath=True, parallel=True)
def para_histogram(times,
                   spec,
                   N_spec,
                   periods,
                   N_periods,
                   weight,
                   min_time=0,
                   max_time=30.,
                   width=0.5,
                   conversion=1.e-3,
                   N_threads=1):
    """
    This method creates histograms from a list of data in parallel.
    It produces a matrix of histograms for multiple periods
    and spectra.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param periods: a list of the periods each event belongs to
    :param N_periods: the number of periods
    :param weight: the weight to give each event in the histogram ( 0 or 1)
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :param conversion: for unit conversions
    :param N_threads: the number of threads to run on
    :returns: a matrix of histograms, the bin edges, the
    number of events in the histogram
    """
    numba.set_num_threads(N_threads)
    """
    Strictly speaking these are not histograms as they
    the y unit is counts and not density.
    This is the language used by the users (muon group at ISIS) and the
    analysis code (Wimda/Mantid) applys the normalisation.

    To avoid a race condition we need to use a
    unique matrix on each thread, then sum them afterwards.
    """
    bins = get_bin_edges(min_time, max_time, width)

    N = 0
    result = np.zeros((N_threads,
                       N_periods,
                       N_spec,
                       len(bins)-1), dtype=np.int32)

    chunk = int(len(times)//N_threads)

    for thread in numba.prange(N_threads):
        # get slices
        start = thread*chunk
        stop = start + chunk
        if thread == N_threads-1:
            stop = len(times)
        for k in range(start, stop):
            time = times[k]*conversion
            w = weight[k]
            if w != 0 and time <= max_time and time >= min_time:
                j_bin = int((time - min_time) // width)
                p = periods[k]
                det = spec[k]
                result[thread, p, det, j_bin] += w
                N += w

    return np.sum(result, axis=0, dtype=np.int32), bins, N
