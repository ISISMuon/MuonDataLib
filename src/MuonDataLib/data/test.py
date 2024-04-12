from sample import Sample, read_sample_from_histogram
from raw_data import RawData, read_raw_data_from_histogram
from source import read_source_from_histogram
from user import read_user_from_histogram
from periods import read_periods_from_histogram
from detector1 import read_detector1_from_histogram

import h5py
file_in = '\\\Olympic\Babylon5\Public\Anthony_Lim\HIFI00183810.nxs'
file_out = '\\\Olympic\Babylon5\Public\Anthony_Lim\HIFI42.nxs'



with h5py.File(file_in, 'r') as f:
    
    sample = read_sample_from_histogram(f)
    raw = read_raw_data_from_histogram(f)
    source = read_source_from_histogram(f)
    user = read_user_from_histogram(f)
    periods = read_periods_from_histogram(f)
    det1 = read_detector1_from_histogram(f)

f = h5py.File(file_out, 'w')
sample.save_nxs2(f)
raw.save_nxs2(f)
source.save_nxs2(f)
user.save_nxs2(f)
periods.save_nxs2(f)
det1.save_nxs2(f)
