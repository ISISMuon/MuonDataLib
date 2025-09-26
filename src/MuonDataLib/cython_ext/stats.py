import numpy as np


def make_histogram(
        times,
        spec,
        N_spec,
        periods,
        weight,
        min_time=0,
        max_time=30.,
        width=0.5,
        conversion=1.e-3):
    """
    This method creates histograms from a list of data.
    It produces a matrix of histograms for multiple periods
    and spectra.
    Strictly speaking these are not histograms as they
    are not normalised to bin width.
    This is the language used by the users and the
    analysis code applys the normalisation.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param periods: a list of the periods each event belongs to
    :param weight: the weight to give each event in the histogram ( 0 or 1)
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :param conversion: for unit conversions
    :returns: a matrix of histograms, the bin edges, the
    number of events in the histogram
    """

    N = 0

    bins = np.arange(min_time, max_time + width, width, dtype=np.double)

    result = np.zeros((np.max(periods)+1, N_spec, len(bins)-1), dtype=np.int32)
    t = times*conversion
    for p in range(np.max(periods)+1):
        w_p = np.where(periods == p, 1, 0)
        for det in range(N_spec):
            w_d = np.where(spec == det, 1, 0)
            hist, _ = np.histogram(t, density=False, bins=bins, weights=weight*w_d*w_p)
            result[p, det, :] = hist[:]
    N = np.sum(result)
    return result, bins, N
