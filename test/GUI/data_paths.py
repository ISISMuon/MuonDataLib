import os


current = os.path.dirname(os.path.realpath(__file__))


shared = os.path.join(os.path.dirname(current),
                      'data_files')


FILE = os.path.join(shared,
                    'HIFI00195790.nxs')

FILTER = os.path.join(shared,
                      'load_filter.json')

BADFILTER = os.path.join(shared,
                         'load_bad_filter.json')

EXPECT = ("peak_property.Amplitudes: 3.14 \n"
          "sample_log_filters.Temp: [0.0044, 0.163] \n"
          "time_filters.keep_filters: {'first': [0.01, 0.02],"
          " 'second': [0.05, 0.06]} \n")
