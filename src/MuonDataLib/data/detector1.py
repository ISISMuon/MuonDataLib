from MuonDataLib.data.utils import (INT32,
                                    stype)
from MuonDataLib.data.hdf5 import HDF5


class Detector_1(HDF5):
    """
    A class for storing the data associated with the detector 1 group
    in a muon NXS v2 file.
    """
    def __init__(self, resolution, raw_time, spec_i,
                 counts, inst, t0, first, last):
        super().__init__()
        """
        Stores the data for the detector 1 group
        :param resolution: the time resolution (micro s)
        :param raw_time: the uncorrected time
        :param spec_i: the spectrum indices
        :param counts: the counts for the data (period, spec, time)
        :param inst: the instrument name
        :param t0: the time zero value
        :param first: the first good bin
        :param last: the last good bin
        """
        self._dict['resolution'] = resolution
        self._dict['raw_time'] = raw_time
        self._dict['spectrum_index'] = spec_i
        self._dict['inst'] = inst
        self._dict['time_zero'] = t0
        self._dict['first_good'] = first
        self._dict['last_good'] = last

        # this will need to change for events ...
        self._dict['counts'] = counts

        self.N_x = len(counts[0][0])
        self.N_hist = len(counts[0])
        self.N_periods = len(counts)

    @property
    def resolution(self):
        """
        Get the resolution in pico seconds
        :return the resolution in pico seconds
        """
        return int(self._dict['resolution']*1e6)

    def save_nxs2(self, file):
        """
        Save the detector 1 values for a muon NXS v2 file
        :param file: the open file to write the data to
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('instrument')
        tmp.attrs['NX_class'] = 'NXinstrument'
        tmp = tmp.require_group('detector_1')
        tmp.attrs['NX_class'] = 'NXdetector'

        resolution = self.save_int('resolution', self.resolution, tmp)
        resolution.attrs.create('units', 'picoseconds'.encode(), dtype='S11')

        raw = self.save_float_array('raw_time', self._dict['raw_time'], tmp)
        raw.attrs.create('units', 'microseconds'.encode(), dtype='S12')
        raw.attrs.create('long_name', 'time'.encode(), dtype='S4')

        self.save_int_array('spectrum_index',
                            self._dict['spectrum_index'],
                            tmp)

        counts = self.save_counts_array('counts', self.N_periods,
                                        self.N_hist, self.N_x,
                                        self._dict['counts'], tmp)
        counts.attrs.create('axes',
                            ('[period index, '
                             'spectrum index, '
                             'raw time bin]').encode(),
                            dtype='S45')
        counts.attrs.create('long_name', self._dict['inst'].encode(),
                            dtype=stype(self._dict['inst']))
        counts.attrs.create('t0_bin', self._dict['time_zero'], dtype=INT32)

        first_bin = int(self._dict['first_good']/self._dict['resolution'])
        counts.attrs.create('first_good_bin',
                            first_bin,
                            dtype=INT32)

        last_bin = int(self._dict['last_good']/self._dict['resolution'])
        counts.attrs.create('last_good_bin',
                            last_bin,
                            dtype=INT32)


def read_detector1_from_histogram(file):
    """
    A method to read the detector 1 values from a
    muon NXS v2 file.
    :param: the open file to read the values from
    :return: a Detector_1 object with the values loaded
    """
    tmp = file['raw_data_1']['instrument']['detector_1']

    # convert to micro seconds
    resolution = tmp['resolution'][0] / 1.e6

    raw_time = tmp['raw_time'][:]
    spec = tmp['spectrum_index'][:]

    tmp = tmp['counts']
    inst = tmp.attrs['long_name'].decode()
    first_good = tmp.attrs['first_good_bin'] * resolution
    last_good = tmp.attrs['last_good_bin'] * resolution
    t0 = tmp.attrs['t0_bin']
    counts = tmp[:]

    # not used...
    # direction =  tmp['orientation'][0].decode()
    # tmp = file['raw_data_1']['detector_1']
    # needed for mantid ?
    # dead_time = tmp['dead_time'][:]
    # grouping = tmp['grouping'][:]
    # time_zero = tmp['time_zero'][:]

    return Detector_1(resolution,
                      raw_time,
                      spec,
                      counts,
                      inst, t0,
                      first_good,
                      last_good)
