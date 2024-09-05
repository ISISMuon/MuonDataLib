from MuonDataLib.data.sample import Sample
from MuonDataLib.data.raw_data import RawData
from MuonDataLib.data.source import Source
from MuonDataLib.data.user import User
from MuonDataLib.data.periods import Periods
from MuonDataLib.data.detector1 import Detector_1 as Detector1
from MuonDataLib.data.muon_data import MuonData
from MuonDataLib.cython_ext.load_events import load_data
from MuonDataLib.data.utils import convert_date

import h5py
import numpy as np


class Data(object):
    def __init__(self, num, start, end):
        self.events = None

        self.run_number = int(num)
        self.start = start
        self.end = end

    def add_events(self, file_name):
        _, self.events = load_data(file_name, 64)

    @property
    def raw_frames(self):
        return self.events.get_total_frames

    def get_histogram(self):
        return self.events.histogram()


def load_events(file_name):
    with h5py.File(file_name, 'r') as file:
        tmp = file.require_group('raw_data_1')
        num = tmp['run_number'][()]
        start = convert_date(tmp['start_time'][()].decode().split('+')[0])
        end = convert_date(tmp['end_time'][()].decode().split('+')[0])

        data = Data(num, start, end)
    data.add_events(file_name)
    return data


def save_events(data):

    run_number = data.run_number
    raw_frames = data.raw_frames
    start_time = data.start
    end_time = data.end
    duration = (end_time - start_time).total_seconds()
    good_frames = data.raw_frames
    requested = data.raw_frames
    # toal_counts appears to be zero in current files
    total_counts = 0.0
    counts, raw_time = data.get_histogram()

    raw_data = RawData(good_frames,
                       2,
                       'pulsedTD',
                       'HIFI',
                       'Title: test',
                       'Notes: test',
                       run_number,
                       duration,
                       raw_frames,
                       start_time,
                       end_time,
                       'raw ID: test')

    sample = Sample('sample ID: test',
                    1.1,
                    2.2,
                    3.3,
                    4.4,
                    5.5,
                    'sample name: test')

    source = Source('ISIS',
                    'Probe',
                    'Pulsed')

    user = User('user name: RAL',
                'affiliation: test')

    periods = Periods(1,
                      'label test',
                      [1],
                      [requested],
                      [raw_frames],
                      [0],
                      [total_counts],
                      [1])

    detector1 = Detector1(0.016,
                          raw_time,
                          np.arange(1, 65),
                          [counts],
                          'HIFI test',
                          3,
                          9*0.016,
                          2018*0.016)

    return MuonData(sample=sample,
                    raw_data=raw_data,
                    source=source,
                    user=user,
                    periods=periods,
                    detector1=detector1)
