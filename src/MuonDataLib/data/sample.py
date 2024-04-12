from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 

from hdf5 import HDF5
import numpy as np
import h5py

#sample_grp_path = '/raw_data_1/sample'
#sample_path = '/raw_data_1/sample/name'
#temperature_path = '/raw_data_1/sample/temperature'
#field_path = '/raw_data_1/sample/magnetic_field'


class Sample(HDF5):
    def __init__(self, ID, thickness, height, width, B_field, Temp, name):
        super().__init__()
        self._dict['ID'] = ID
        self._dict['thickness'] = thickness
        self._dict['height'] = height
        self._dict['width'] = width
        self._dict['B_field'] = B_field
        self._dict['Temp'] = Temp
        self._dict['name'] = name

    def save_nxs2(self, file):

        #sample = file.create_group(sample_group_path)
        #sample.attrs.create('NX_class', 'NXsample', dtype='S9')
        #file.create_dataset(sample_path, (1), dtype=stype(self._name), data=self._name)
        #file.create_dataset(temperature_path, (1), data=self._Temp)
        #file.create_dataset(field_path, (1), data=self._B_field)

        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('sample')
        tmp.attrs['NX_class'] = 'NXsample'

        self.save_str('id', self._dict['ID'], tmp)
        self.save_str('name', self._dict['name'], tmp)
        self.save_float('thickness', self._dict['thickness'], tmp)
        self.save_float('height', self._dict['height'], tmp)
        self.save_float('width', self._dict['width'], tmp)
        self.save_float('magnetic_field', self._dict['B_field'], tmp)
        self.save_float('temperature', self._dict['Temp'], tmp)




def read_sample_from_histogram(file):
    tmp = file['raw_data_1']['sample']
    return Sample(tmp['id'][0].decode(), 
                  tmp['thickness'][0],
                  tmp['height'][0],
                  tmp['width'][0],
                  tmp['magnetic_field'][0],
                  tmp['temperature'][0],
                  tmp['name'][0].decode())



