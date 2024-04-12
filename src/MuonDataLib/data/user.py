from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
from hdf5 import HDF5 

import numpy as np
import h5py

 
class User(HDF5):
    def __init__(self, name, affiliation):
        super().__init__()
        self._dict['name'] = name
        self._dict['affiliation'] = affiliation
        
    def save_nxs2(self, file):
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('user_1')
        tmp.attrs['NX_class'] = 'NXuser'
        
        for key in self._dict.keys():
            self.save_str(key, self._dict[key], tmp)
            # wimda save has them as attributes...
            #tmp.attrs[key] = self._dict[key]

def read_user_from_histogram(file):
    tmp = file['raw_data_1']
    tmp = tmp['user_1']

    return User(tmp['name'][0].decode(),  
                tmp['affiliation'][0].decode())

