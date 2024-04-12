from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 
from hdf5 import HDF5
import numpy as np
 

class RawData(HDF5):
    def __init__(self, good_frames, IDF, definition, inst, title, notes,
                 run_number, duration, raw_frames, start_time, end_time, ID):
        super().__init__()
        self._dict['good_frames'] = good_frames
        self._dict['IDF'] = IDF
        self._dict['def'] = definition
        self._dict['inst'] = inst
        self._dict['title'] = title
        self._dict['notes'] = notes
        self._dict['run_number'] = run_number
        self._dict['duration'] = duration
        self._dict['raw_frames'] = raw_frames
        self._dict['start'] = start_time
        self._dict['end'] = end_time
        self._dict['ID'] = ID

    def save_nxs2(self, file):

        tmp = file.require_group('raw_data_1')
        tmp.attrs['NX_class'] = 'NXentry'

        self.save_int('good_frames', self._dict['good_frames'], tmp)
        self.save_int('IDF_version', self._dict['IDF'], tmp)
        self.save_str('definition', self._dict['def'], tmp)
        self.save_str('name', self._dict['inst'], tmp)
        self.save_str('title', self._dict['title'], tmp)
        self.save_str('notes', self._dict['notes'], tmp)
        self.save_int('run_number', self._dict['run_number'], tmp)
        # duration
        self.save_int('raw_frames', self._dict['raw_frames'], tmp)
        self.save_str('start_time', convert_date_for_NXS(self._dict['start']), tmp)
        self.save_str('end_time', convert_date_for_NXS(self._dict['end']), tmp)
        self.save_str('experiment_identifier', self._dict['ID'], tmp)



def read_raw_data_from_histogram(file):
    tmp = file['raw_data_1']
    return RawData(tmp['good_frames'][0],
                   tmp["IDF_version"][0],
                   tmp['definition'][0].decode(),
                   tmp['name'][0].decode(),
                   tmp['title'][0].decode(),
                   tmp['notes'][0].decode(),
                   tmp['run_number'][0],
                   tmp['duration'][0],
                   tmp['raw_frames'][0],
                   convert_date(tmp['start_time'][0].decode()),
                   convert_date(tmp['end_time'][0].decode()),
                   tmp['experiment_identifier'][0].decode())


"""
raw_data_grp_path = '/raw_data_1'
idf_version_path = '/raw_data_1/IDF_version'
definition_path = '/raw_data_1/definition'
id_path = '/raw_data_1/experiment_identifier'
title_path = '/raw_data_1/title'
frames_path = '/raw_data_1/good_frames'
run_number_path = '/raw_data_1/run_number'
start_time_path = '/raw_data_1/start_time'
end_time_path = '/raw_data_1/end_time'

  
  rdgrp = f.create_group(raw_data_grp_path)
  rdgrp.attrs.create('NX_class','NXentry',dtype='S8')

  f.create_dataset(idf_version_path, (1), dtype='int32', data=idf_version)
  f.create_dataset(definition_path, (1), dtype=stype(definition), data=definition)
  f.create_dataset(id_path, (1), dtype='S12', data=data._ID)
  

  f.create_dataset(run_number_path, (1), dtype='int32', data=data._run_number)
  f.create_dataset(title_path, (1), dtype='S12', data=data._notes)
  
  f.create_dataset(frames_path, (1), dtype='int32', data=data._good_frames)

"""
