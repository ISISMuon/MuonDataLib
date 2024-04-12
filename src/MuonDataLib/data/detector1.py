from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 
from hdf5 import HDF5



 
class Detector_1(HDF5):
    def __init__(self, resolution, raw_time, spec_i, counts, inst, t0, first, last):
        super().__init__()
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
        return self._dict['resolution']*1e6

    def save_nxs2(self, file):
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('instrument')
        tmp.attrs['NX_class'] = 'NXinstrument'
        tmp = tmp.require_group('detector_1')
        tmp.attrs['NX_class'] = 'NXdetector'
        
        resolution = self.save_int('resolution', self.resolution, tmp)
        resolution.attrs.create('units', 'picoseconds', dtype='S11')

        raw = self.save_float_array('raw_time', self._dict['raw_time'], tmp)
        raw.attrs.create('units', 'microseconds', dtype='S12')
        raw.attrs.create('long_name', 'time', dtype='S4')

        self.save_int_array('spectrum_index', self._dict['spectrum_index'], tmp)

        counts = self.save_counts_array('counts', self.N_periods, self.N_hist, self.N_x, self._dict['counts'], tmp)
        counts.attrs.create('axes', '[period index, spectrum index, raw time bin]', dtype='S45')
        counts.attrs.create('long_name', self._dict['inst'], dtype=stype(self._dict['inst']))
        counts.attrs.create('t0_bin', self._dict['time_zero'], dtype=INT32)
        counts.attrs.create('first_good_bin', int(self._dict['first_good']/self._dict['resolution']), dtype=INT32)
        counts.attrs.create('last_good_bin', int(self._dict['last_good']/self._dict['resolution']), dtype=INT32)
 




def read_detector1_from_histogram(file):
    tmp = file['raw_data_1']['instrument']['detector_1']

    # not used...
    direction =  tmp['orientation'][0].decode()

    # used
    resolution = tmp['resolution'][0]/ 1.e6 # convert to micros 
    raw_time = tmp['raw_time'][:]
    spec = tmp['spectrum_index'][:]

    tmp = tmp['counts']
    inst = tmp.attrs['long_name']
    first_good = tmp.attrs['first_good_bin'] * resolution
    last_good = tmp.attrs['last_good_bin'] * resolution  
    t0 = tmp.attrs['t0_bin']
    counts = tmp[:]

    #########################################################
    tmp = file['raw_data_1']['detector_1']
    # needed for mantid
    dead_time = tmp['dead_time'][:]
    grouping = tmp['grouping'][:]

    #time_zero = tmp['time_zero'][:]
 
    return Detector_1(resolution, raw_time, spec, counts, inst, t0, first_good, last_good)

