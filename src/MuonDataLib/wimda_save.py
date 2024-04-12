from utils import (INT32, FLOAT32,
                   convert_date_for_NXS,
                   convert_date,
                   stype)
 
from hdf5 import HDF5
#from mantid.simpleapi import *

#import matplotlib.pyplot as plt

import numpy as np

import time

import h5py

 
int32 = np.int32

float32 = np.float32
 
def convertDateForNXS(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S')
 
class Sample(object):
    def __init__(self, ID, thickness, height, width, B_field, Temp, name):
        self._ID = ID
        self._thickness = thickness
        self._height = height
        self._width = width
        self._B_field = B_field
        self._Temp = Temp
        self._name = name
 

class Source(object):
    def __init__(self, name, probe, type):
        self._name = name
        self._probe = probe
        self._type = type


class User(object):
    def __init__(self, name, affiliation):
        self._name = name
        self._affiliation = affiliation
        
    def save_nxs_2(self, file):
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('user_1')
        
        tmp.attrs['NX_class'] = 'NXuser'
        tmp.attrs['name'] = self._name
        tmp.attrs['affiliation'] = self._affiliation
        _ = tmp.require_dataset('name', shape=(1), data=np.array([self._name], dtype='S12'), dtype='S12')        
        _ = tmp.require_dataset('affiliation', shape=(1), data=np.array([self._affiliation], dtype='S12'), dtype='S12')        

class Periods(object):
    def __init__(self, number, labels, type, requested, raw, output, counts, sequences):
        self._number = number
        self._labels = labels#.split(';')
        self._type = type
        self._requested = requested
        self._raw = raw
        self._output = output
        self._counts = counts
        self._sequences = sequences
        
        self._active = 0
        for frames in self._raw:
            if frames > 0:
                self._active += 1
        
    def num(self):
        return self._active
        
    def _print(self):
        print('number', self._number)
        print('labels', self._labels)#.join(';'))
        print('type', self._type)
        print('requested frames', self._requested)
        print('raw frames', self._raw)
        print('output', self._output)
        print('counts', self._counts)
        print('sequences', self._sequences)
        print('active', self._active)
        
    def save_nxs_2(self, file):
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('periods')
        
        tmp.attrs['NX_class'] = 'NXperiod'
        _ = tmp.require_dataset('number', shape=(1), data=1, dtype=int32)
        _ = tmp.require_dataset('sequences', shape=(len(self._sequences)), data=self._sequences, dtype=int32)
        _ = tmp.require_dataset('labels', shape=(1), data=self._labels.encode(), dtype='S12')

        _ = tmp.require_dataset('type', shape=(len(self._type)), data=self._type, dtype=int32)
        _ = tmp.require_dataset('frames_requested', shape=(len(self._requested)), data=self._requested, dtype=int32)
        _ = tmp.require_dataset('raw_frames', shape=(len(self._raw)), data=self._raw, dtype=int32)
        _ = tmp.require_dataset('output', shape=(len(self._output)), data=self._output, dtype=int32)
        _ = tmp.require_dataset('total_counts', shape=(len(self._counts)), data=self._counts, dtype=float32)        

class MuonData(object):

    def __init__(self):

        self._x = []

        self._y = {}
        
        self._raw_time = []

        self._dead_time = None

        self._grouping = None

        self._time_zero = 0.0

        self._good_frames = 0

        self._instrument = None

        self._notes = None
        self._title = ''

        self._run_number = 0
        self._def = ''

        self._direction = ''

        self._time_resolution = 0

        self._first_good = 0

        self._last_good = 0

        self._resolution = 0

        self._sample_log = {}
        self._end_time = None
        self._start_time = None
        self._duration = 0.0
        self._spec = []

        self._source = None
        self._raw_frames = 0
        self._ID = 0
        self._sample = None
        self._periods = None
        self._user = None
        
        self._IDF = None
        self._def = None
        
        self._inst = ''

    def get_data(self, index, period=1):

        return self._x, self._y[period-1][index]

 
def getUser(file, data):
    tmp = file['raw_data_1']
    tmp = tmp['user_1']

    data._user = User(tmp['name'][0].decode(),  
                      tmp['affiliation'][0].decode())

def getRawData(file, data):

    tmp = file['raw_data_1']

    data._good_frames = tmp['good_frames'][0]
    data._IDF = tmp["IDF_version"][0]
    data._def = tmp['definition'][0].decode()
    data._instrument = tmp['name'][0].decode()
    data._title = tmp['title'][0].decode()
    
    data._notes = tmp['notes'][0].decode()

    data._run_number = tmp['run_number'][0]
    data._duration = tmp['duration'][0]
    data._raw_frames = tmp['raw_frames'][0]
    data._def = tmp['definition'][0].decode()
    data._end_time = convertDate(tmp['end_time'][0].decode())
    data._start_time = convertDate(tmp['start_time'][0].decode())
    data._ID = tmp['experiment_identifier'][0].decode()

def getSample(file, data):
    tmp = file['raw_data_1']['sample']
    data._sample = Sample(tmp['id'][0].decode(), 
                          tmp['thickness'][0],
                          tmp['height'][0],
                          tmp['width'][0],
                          tmp['magnetic_field'][0],
                          tmp['temperature'][0],
                          tmp['name'][0].decode())

def getSource(file, data):
    tmp = file['raw_data_1']['instrument']['source']
    data._source = Source(tmp['name'][0].decode(),
                          tmp['probe'][0].decode(),
                          tmp['type'][0].decode())
                         
                       
def get_instrument(file, data):
    tmp = file['raw_data_1']['instrument']
    data._inst = tmp['name'][0].decode()                      

def getInstrumentDetector1(file, data):

        tmp = file['raw_data_1']['instrument']['detector_1']

        data._direction =  tmp['orientation'][0].decode()

        data._resolution = tmp['resolution'][0]/ 1.e6 # convert to micros 
        
        data._raw_time = tmp['raw_time'][:]
        data._spec = tmp['spectrum_index'][:]

        tmp2 = tmp['counts']

        data._first_good = tmp2.attrs['first_good_bin'] * data._resolution

        data._last_good = tmp2.attrs['last_good_bin'] * data._resolution  

           
def getDetector1(file, data):

        counts = file['raw_data_1']['detector_1']['counts']

        N_hist = len(counts[0])

        N_x = len(counts[0][0])

       

        tmp = file['raw_data_1']['detector_1']

        data._dead_time = tmp['dead_time'][:]

        data._grouping = tmp['grouping'][:]

        data._time_zero = tmp['time_zero'][:]

        # get x data (same for all spec)

        data._x = tmp['corrected_time'][:]

        # get count data

        for period in range(data._periods.num()):
            data._y[period] = {}
            for spec in range(N_hist):
                data._y[period][spec] = np.zeros(N_x)

        for period in range(data._periods.num()):
            for spec in range(N_hist):

                data._y[period][spec][:] = counts[period][spec][:]   
            

def getPeriods(file, data):

    tmp = file['raw_data_1']['periods']

    data._periods = Periods(number=tmp['number'][:][0],
                             labels=tmp['labels'][:][0].decode(),
                             type=tmp['type'][:],
                             requested=tmp['frames_requested'][:],
                             raw=tmp['raw_frames'][:],
                             output=tmp['output'][:],
                             counts=tmp['total_counts'][:],
                             sequences=tmp['sequences'][:])


def convertDate(date):

    """

    Assume in the form f'{year} {month} {day}', time

    """

    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

 

def readSampleLog(selog, log_name):
    tmp = selog[log_name]
    start = convertDate(tmp['value_log']['time'].attrs['start'].decode())
    tmp_times = tmp['value_log']['time'][:]
    values = tmp['value_log']['value'][:]
    tmp_values = tmp['value_log']['value'][:]
    
    check = True
    while check:
        print('hi', log_name, type(tmp_values), tmp_values[0])
        if type(tmp_values[0]) == np.bytes:
            values = values.decode()
            print('baaaaaaaaa', values, log_name)
        elif type(tmp_values) != np.ndarray:
            check=False

        print('check', check)#, log_name, type(tmp_values[0]), tmp_values[0])

        tmp_values = tmp_values[0]
    times = 1

    times = [None for j in range(len(tmp_times))]   

    for j, time in enumerate(tmp_times):

        times[j] = datetime.datetime.strftime(start + datetime.timedelta(0, float(time)), '%Y-%B-%d %H:%M:%S')
    return times, values

 

def getSelog(file, data):

    selog = file['raw_data_1']['selog']

    count = 0

    for name in list(selog.keys()):
        try:

            data._sample_log[name] = readSampleLog(selog, name)


            count += 1

        except:

            continue
          

def MuonLoad(file_name):

    data = MuonData()

    with h5py.File(file_name, 'r') as f:

       
        getPeriods(f, data)
        getUser(f, data)
        getRawData(f, data)
        getSample(f, data)
        getSource(f, data)
        get_instrument(f, data)
        getInstrumentDetector1(f, data)

 

        getDetector1(f, data)


        getSelog(f, data)

 

    return data

 

 

 

         

          


data = MuonLoad('/mnt/ceph/home/al1102200/Downloads/HIFI00180594.nxs')
#data = MuonLoad('/mnt/ceph/home/al1102200/Downloads/HIFI00183810.nxs')
muonSave('/mnt/ceph/home/al1102200/Downloads/HIFI010.nxs', data)
raw_data_grp_path = '/raw_data_1'
idf_version_path = '/raw_data_1/IDF_version'
definition_path = '/raw_data_1/definition'
id_path = '/raw_data_1/experiment_identifier'
title_path = '/raw_data_1/title'
user_1_path = '/raw_data_1/user_1'
frames_path = '/raw_data_1/good_frames'
run_number_path = '/raw_data_1/run_number'
start_time_path = '/raw_data_1/start_time'
end_time_path = '/raw_data_1/end_time'

sample_grp_path = '/raw_data_1/sample'
sample_path = '/raw_data_1/sample/name'
temperature_path = '/raw_data_1/sample/temperature'
field_path = '/raw_data_1/sample/magnetic_field'

periods_grp_path = '/raw_data_1/periods'
periods_path = '/raw_data_1/periods/number'

instrument_grp_path = '/raw_data_1/instrument'
instrument_name_path = '/raw_data_1/instrument/name'
source_grp_path = '/raw_data_1/instrument/source'
source_name_path = '/raw_data_1/instrument/source/name'

detector_1_path = '/raw_data_1/instrument/detector_1'
counts_path = '/raw_data_1/instrument/detector_1/counts'
raw_time_path = '/raw_data_1/instrument/detector_1/raw_time'
resolution_path = '/raw_data_1/instrument/detector_1/resolution'
spectrum_index_path = '/raw_data_1/instrument/detector_1/spectrum_index'


save_path = '/mnt/babylon/Public/Anthony_Lim/HIFI0004.nxs'

def stype(s):
    return 'S{}'.format(len(s)+1)	

def parse(s,n):
    i1 = -1
    while n > 0:
      i0 = i1+1
      i1 = s.find(',',i0)
      if i1 == -1:
        i1 = len(s)
      n = n-1
    return s[i0:i1]

# Nexus info:
idf_version = 2
definition = 'pulsedTD'

with h5py.File(save_path, 'w') as f:

  #print('Creating file: ', nexusfile,' from: ',rootfile)
  
  rdgrp = f.create_group(raw_data_grp_path)
  rdgrp.attrs.create('NX_class','NXentry',dtype='S8')

  f.create_dataset(idf_version_path, (1), dtype='int32', data=idf_version)
  f.create_dataset(definition_path, (1), dtype=stype(definition), data=definition)
  f.create_dataset(id_path, (1), dtype='S12', data=data._ID)
  
  user_1 = f.create_group(user_1_path)
  user_1.attrs.create('NXclass', 'NXuser', dtype='S7')
  user_1.attrs.create('name', data._user._name, dtype='S12')
  user_1.attrs.create('affiliation', data._user._affiliation, dtype='S12')

  f.create_dataset(run_number_path, (1), dtype='int32', data=data._run_number)
  f.create_dataset(title_path, (1), dtype='S12', data=data._notes)
  
  f.create_dataset(frames_path, (1), dtype='int32', data=data._good_frames)

  sampgrp = f.create_group(sample_grp_path)
  sampgrp.attrs.create('NX_class', 'NXsample', dtype='S9')
  f.create_dataset(sample_path, (1), dtype='S12', data=data._sample._name)
  f.create_dataset(temperature_path, (1), data=data._sample._Temp)
  f.create_dataset(field_path, (1), data=data._sample._B_field)

  instgrp = f.create_group(instrument_grp_path)
  instgrp.attrs.create('NX_class', 'NXinstrument', dtype='S13')
  f.create_dataset(instrument_name_path, (1), dtype='S6', data=data._instrument)
  f.create_dataset(start_time_path, (1), dtype='S20', data=convertDateForNXS(data._start_time))

  f.create_dataset(end_time_path, (1), dtype='S20', data=convertDateForNXS(data._end_time))

  
  tmp = f.create_group(periods_grp_path)
  tmp.attrs.create('NX_class', 'NXperiod', dtype='S9')
  _ = tmp.require_dataset('frames_requested', shape=(len(data._periods._requested)), data=data._periods._requested, dtype=int32)

  _ = tmp.require_dataset('number', shape=(1), data=data._periods._number, dtype=int32)
  _ = tmp.require_dataset('sequences', shape=(len(data._periods._sequences)), data=data._periods._sequences, dtype=int32)
  _ = tmp.require_dataset('labels', shape=(1), data=data._periods._labels.encode(), dtype='S12')

  _ = tmp.require_dataset('type', shape=(len(data._periods._type)), data=data._periods._type, dtype=int32)
  _ = tmp.require_dataset('raw_frames', shape=(len(data._periods._raw)), data=data._periods._raw, dtype=int32)
  _ = tmp.require_dataset('output', shape=(len(data._periods._output)), data=data._periods._output, dtype=int32)
  _ = tmp.require_dataset('total_counts', shape=(len(data._periods._counts)), data=data._periods._counts, dtype=float32)

         
  source = f.create_group(source_grp_path)
  source.attrs.create('NX_class', 'NXsource', dtype='S9')
  source.attrs.create('name', dtype='S12', data=data._source._name)
  source.attrs.create('probe', dtype='S12', data=data._source._probe)
  source.attrs.create('type', dtype='S12', data=data._source._type)
  
  detgrp = f.create_group(detector_1_path)
  detgrp.attrs.create('NX_class','NXdetector',dtype='S11')
  resn = f.create_dataset(resolution_path, (1), dtype=int32, data=np.array(data._resolution*1.e6, dtype=int32))
  resn.attrs.create('units','picoseconds',dtype='S12')
  
  raw = f.create_dataset(raw_time_path, (len(data._raw_time)), dtype=float32, data=data._raw_time)
  raw.attrs.create('units', 'microsecond', dtype='S12')
  raw.attrs.create('long_name', 'time', dtype='S5')
  f.create_dataset(spectrum_index_path, (len(data._spec)), dtype=int32, data = data._spec)

  # do logs
  """
  segrp = f.create_group('/raw_data_1/selog')
  segrp.attrs.create('NX_class', 'IXselog', dtype='S8')
  for logname in data._sample_log.keys():
    print("mw", logname)
    lognam = f'/raw_data_1/selog/{logname}'
    log_grp = f.create_group(logname)
    log_grp.attrs.create('NX_class', 'IXselog', dtype='S8')
    log_grp_v = f.create_group(logname+'/value_log')
    log_grp_v.attrs.create('NX_class', 'NXlog', dtype='S6')
    times, values = data._sample_log[logname]
    f.create_dataset(logname+'/value_log/time', (len(times)), dtype = 'S32', data = times)
    data_type = ''
    while data_type == '':
        if type(values[0]) == int:
            data_type = int32
        elif type(values[0]) == str:
            data_type = 'S12'
            values = values.encode()
        elif type(values[0]) == float32:
            data_type= float32
        elif type(values[0]) == bool:
            data_type = bool
        else:
            values = values[0]
    print('moo', logname, values, data_type, type(values[0]))

    f.create_dataset(logname+'/value_log/value', (len(values)), dtype = data_type, data = values)
  """

  N_hist = len(data._y[0])
  count_data = np.zeros((data._periods.num(), N_hist, len(data._x)))
  for period in range(data._periods.num()):
      for spec in range(N_hist):
         count_data[period][spec][:] = data._y[period][spec][:] 
  
  counts = f.create_dataset(counts_path, shape=(data._periods.num(), N_hist, len(data._x)), data=count_data, dtype=int32)
  counts.attrs.create('axes', '[period index, spectrum index, raw time bin]', dtype='S45')
  counts.attrs.create('long_name', data._inst, dtype='S12')
  counts.attrs.create('t0_bin', data._time_zero, dtype='int32')
  counts.attrs.create('first_good_bin', int(data._first_good/data._resolution), dtype='int32')
  counts.attrs.create('last_good_bin', int(data._last_good/data._resolution), dtype='int32')
 

  #print('\n Done')

