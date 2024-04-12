from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 
from hdf5 import HDF5
import numpy as np


class Periods(HDF5):
    def __init__(self, number, labels, p_type, requested, raw, output, counts, sequences):
        super().__init__()
        self._dict['number'] = number
        self._dict['labels'] = labels#.split(';')
        self._dict['type'] = p_type
        self._dict['requested'] = requested
        self._dict['raw'] = raw
        self._dict['output'] = output
        self._dict['counts'] = counts
        self._dict['sequences'] = sequences
        
    def save_nxs2(self, file):
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('periods')
        
        tmp.attrs['NX_class'] = 'NXperiod'
        self.save_int('number', self._dict['number'], tmp)
        self.save_int_array('sequences', self._dict['sequences'], tmp)
        self.save_str('labels', self._dict['labels'], tmp)
        self.save_int_array('type', self._dict['type'], tmp)
        self.save_int_array('frames_requested', self._dict['requested'], tmp)
        self.save_int_array('raw_frames', self._dict['raw'], tmp)
        self.save_int_array('output', self._dict['output'], tmp)
        self.save_float_array('total_conts', self._dict['counts'], tmp)


def read_periods_from_histogram(file):

    tmp = file['raw_data_1']['periods']

    return Periods(number=tmp['number'][:][0],
                   labels=tmp['labels'][:][0].decode(),
                   p_type=tmp['type'][:],
                   requested=tmp['frames_requested'][:],
                   raw=tmp['raw_frames'][:],
                   output=tmp['output'][:],
                   counts=tmp['total_counts'][:],
                   sequences=tmp['sequences'][:])

        
