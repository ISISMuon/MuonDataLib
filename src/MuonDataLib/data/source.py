from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 
from hdf5 import HDF5

import numpy as np


class Source(HDF5):
    def __init__(self, name, probe, s_type):
        super().__init__()
        self._dict['name'] = name
        self._dict['probe'] = probe
        self._dict['type'] = s_type

    def save_nxs2(self, file):
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('instrument')
        
        ############ test ##################
        self.save_str('name', 'HIFI', tmp)
        ###################################

        tmp = tmp.require_group('source')
        tmp.attrs['NX_class'] = 'NXsource'
        # for some reason wimda save has these as attributes
        for key in self._dict.keys():
            self.save_str(key, self._dict[key], tmp)


def read_source_from_histogram(file):
    tmp = file['raw_data_1']['instrument']['source']
    return Source(tmp['name'][0].decode(),
                  tmp['probe'][0].decode(),
                          tmp['type'][0].decode())
                         
