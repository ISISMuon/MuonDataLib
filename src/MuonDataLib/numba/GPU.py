#from MuonDataLib.numba.stats import get_bin_edges
import numpy as np
import time
import numba
from numba import cuda
from numba.core.errors import NumbaPerformanceWarning
from tqdm.auto import trange
from numba.cuda.types import int32, float64, int64, float32


@cuda.jit
def GPU_hist(x, y, x_0, x_N, hist):
    nbins = hist.shape[0]
    width = (x_N - x_0)/nbins

    start = cuda.grid(1)
    stride = cuda.gridsize(1)

    for k in range(start, x.size, stride):
        element = x[k]
        j = int((element - x_0)/width)
        if j >= 0 and j < nbins:
 
            cuda.atomic.add(hist,(y[k], j), 1)

@cuda.jit((float32[:], float32[:]), fastmath=True, cache=True)
def get_bin_edges(info, bin_edges):
    """
    A method to caclculate histogram bin edges,
    given the range and bin width.
    :param a_min: the first bin edge
    :param a_max: the last bin edge
    :param width: the bin width
    :return: the bin edges
    """
    start = cuda.grid(1)
    stride = cuda.gridsize(1)

    for i in range(start, bin_edges.size, stride):
        bin_edges[i] = info[0] + i * info[2]

    bin_edges[bin_edges.size-1] = info[1]  # Avoid roundoff error on last point


@cuda.jit(fastmath=True, cache=True)
def calc_hist(times,
              spec,
              periods,
              weight,
              info,
              hist,
              N
              ):
    start = cuda.grid(1)
    stride = cuda.gridsize(1)
    # shared memory to reduce global atomic contention
    tid = cuda.threadIdx.x
    shared_N = cuda.shared.array(1, dtype=int32)

    # initialize the first occurance
    if tid==0:
        shared_N[0] = 0
    cuda.syncthreads()

    for k in range(start, times.size, stride):
        time = times[k]*info[3]
        if time >= info[0] and time <= info[1]:
            j_bin = int((time - info[0])/ info[2])
            w = weight[k]
        else:
            j_bin = 0
            w = 0
        cuda.atomic.add(hist, (periods[k], spec[k], j_bin), weight[k])
        cuda.atomic.add(shared_N, 0, weight[k])

    # once all threads are done some the local copies of N
    cuda.syncthreads()
    if tid==0:
        cuda.atomic.add(N, 0, shared_N[0])

def GPU_histogram(times,
                  spec,
                  N_spec,
                  periods,
                  N_periods,
                  weight,
                  min_time=0,
                  max_time=30.,
                  width=0.5,
                  conversion=1.e-3):
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
    """
    Strictly speaking these are not histograms as they
    the y unit is counts and not density.
    This is the language used by the users (muon group at ISIS) and the
    analysis code (Wimda/Mantid) applys the normalisation.

    To avoid a race condition we need to use a
    unique matrix on each thread, then sum them afterwards.
    """
    # threads per block
    TPB = 256

    GPU_info = cuda.to_device(np.array([min_time, max_time, width, conversion],dtype=np.float32))

    bins = np.zeros(int((max_time - min_time)/width) + 1, dtype=np.float32)
    GPU_bins = cuda.to_device(bins)
    get_bin_edges.forall(len(GPU_bins))(GPU_info, GPU_bins)
    bins = np.array(GPU_bins.copy_to_host(), dtype=np.float64)
    del GPU_bins

    N = np.zeros(1)
    result = np.zeros((N_periods, N_spec, len(bins) - 1), dtype=np.int32)

    GPU_result =cuda.to_device(result)
    GPU_N = cuda.to_device(N)
    
    # largest array we can use without running out of memory
    step = int(3.75e8)
    for k in range(int(np.ceil(len(times)/step))):
        start = k*step
        stop = (k+1)*step
        GPU_times = cuda.to_device(times[start:stop])
        GPU_spec = cuda.to_device(spec[start:stop])
        GPU_periods = cuda.to_device(periods[start:stop])
        GPU_weight = cuda.to_device(weight[start:stop])
        
        # blocks per grid
        BPG = int(np.ceil(len(GPU_times) / TPB))

        # Need to explicitly set kernel config for shared memory
        calc_hist[BPG, TPB](GPU_times,
                  GPU_spec,
                  GPU_periods,
                  GPU_weight,
                  GPU_info,
                  GPU_result,
                  GPU_N
                  )
        del GPU_times
        del GPU_spec
        del GPU_periods
        del GPU_weight
    result = GPU_result.copy_to_host()
    N = GPU_N.copy_to_host()
    del GPU_result
    del GPU_N
    
    del GPU_info
    return result, bins, N[0]

