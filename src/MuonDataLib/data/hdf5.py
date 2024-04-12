from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 


import numpy as np
import h5py


class HDF5(object):
    def __init__(self):
        self._dict = {}

    def save_str(self, name, string, group):
        dtype = stype(string)
        return group.require_dataset(name=name, shape=(1), data = np.array([string.encode()], dtype=dtype), dtype=dtype)

    def save_float(self, name, value, group):
        return group.require_dataset(name=name, shape=(1), data=[value], dtype=FLOAT32)

    def save_int(self, name, value, group):
        return group.require_dataset(name=name, shape=(1), data=[value], dtype=INT32)

    def save_int_array(self, name, values, group):
        return group.require_dataset(name=name, shape=len(values), data=values, dtype=INT32)

    def save_counts_array(self, name, N_periods, N_hist, N_x, values, group):
        return group.require_dataset(name=name, shape=(N_periods, N_hist, N_x), 
                                     data=values, dtype=INT32)

    def save_float_array(self, name, values, group):
        return group.require_dataset(name=name, shape=len(values), data=values, dtype=FLOAT32)


