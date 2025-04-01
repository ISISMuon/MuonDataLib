from MuonDataLib.help.help_doc import (Doc,
                                       HIST,
                                       NXS,
                                       FILTER,
                                       TIME,
                                       LOG)


MUONDATA = 'MuonData'


def get_muon_data_docs():

    return [Doc('MuonData',
                'data.muon_data',
                [MUONDATA],
                "An object that stores the relevant information "
                "for muon data (as definied by NeXus version 2)."
                "This is automatically created by `load_events`.",
                {"sample": "The sample data.",
                 "raw_data": "The raw data (as defined by NeXus group).",
                 "source": "The source data (as defined by NeXus group).",
                 "periods": "The period data (as defined by NeXus group).",
                 "detector1": "The detector 1 data (as defined by "
                 "NeXus group)."},
                returns="MuonData object.",
                example=['from MuonDataLib.data.muon_data '
                         'import MuonData',
                         'sample. raw, src, period, det = get_data()',
                         'muon = MuonData(sample, raw, src, period, det)']),

            Doc('save_histograms',
                'data.muon_data.MuonData',
                [MUONDATA, HIST, NXS],
                "Method for saving a MuonData object to a "
                "NeXus v2 histogram file "
                "This will skip calculating the filters "
                "if the cache is occupied. "
                "If just the resolution has changed it will "
                "not alter the filtered values.",
                {'file_name': "The name of the file to save the "
                              "NeXus v2 histogram file to."},
                optional_param={'resolution': ["The resolution (bin width), "
                                               "in microseconds, to use "
                                               "in the histograms.",
                                               "0.016 microseconds"]},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.save_histograms("HIFI00001_all.nxs",'
                         ' resolution=0.01)']),

            Doc('histogram',
                'data.muon_data.MuonData',
                [MUONDATA, HIST],
                "A method for constructing a histogram from a "
                "MuonData object. "
                "This method is helpful for checking results. "
                "This will skip calculating the filters "
                "if the cache is occupied. "
                "If just the resolution has changed it will "
                "not alter the filtered values.",
                optional_param={'resolution': ["The resolution (bin width), "
                                               "in microseconds, to use "
                                               "in the histograms.",
                                               "0.016 microseconds"]},
                returns="A matrix of histograms (period, "
                        "spectrum number, bin) and bin edges.",
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'hist, bins = data.histogram(resolution=0.01)']),

            Doc('clear_filters',
                'data.muon_data.MuonData',
                [MUONDATA, FILTER, TIME, LOG],
                "A method to remove all of the filters from the "
                "MuonData object.",
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         '# Add a filter',
                         'data.only_keep_data_time_between(1.0, 10.)',
                         '# Remove the filter',
                         'data.clear_filters()']),

            Doc('add_sample_log',
                'data.muon_data.MuonData',
                [MUONDATA, LOG],
                "A method to manually add a sample log to a MuonData object.",
                {'name': 'The name of the sample log.',
                 'x_data': 'The x values for the sample log (time in '
                 'seconds).',
                 'y_data': 'The y values for the sample log'},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'import numpy as np',
                         'data = load_events("HIFI00001.nxs"), 64',
                         'x_data, y_data = np.load("Temp.txt")',
                         'data.add_sample_log("Temp", x_data, y_data)']),

            Doc('keep_data_sample_log_below',
                'data.muon_data.MuonData',
                [MUONDATA, LOG, FILTER, HIST],
                "A method to remove all frames containing data "
                "with a value above some threshold value for a "
                "specific sample log, "
                "when creating a histogram from a MuonData object.",
                param={'log_name': "The name of the sample log to apply "
                       "the fitler to.",
                       'max_value': "The maximum log value that will be kept "
                       "after the filter is applied. In the same units as the "
                       "y values for the sample log."},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.keep_data_sample_log_below("Temp", 5)',
                         'hist, bins = data.histogram()']),

            Doc('keep_data_sample_log_above',
                'data.muon_data.MuonData',
                [MUONDATA, LOG, FILTER, HIST],
                "A method to remove all frames containing data "
                "with a value below some threshold value for a "
                "specific sample log, "
                "when creating a histogram from a MuonData object.",
                param={'log_name': "The name of the sample log "
                       "to apply the fitler to.",
                       'min_value': "The minimum log value that will be kept "
                       "after the filter is applied. In the same units as the "
                       "y values for the sample log."},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.keep_data_sample_log_above("Temp", 1.5)',
                         'hist, bins = data.histogram()']),

            Doc('keep_data_sample_log_between',
                'data.muon_data.MuonData',
                [MUONDATA, LOG, FILTER, HIST],
                "A method to only keep frames containing data "
                "between a pair of values for a specific sample log, "
                "when creating a histogram from a MuonData object.",
                param={'log_name': "The name of the sample log to "
                       "apply the fitler to.",
                       'min_value': "The minimum log value that will be kept "
                       "after the filter is applied. In the same units as the "
                       "y values for the sample log.",
                       'max_value': "The maximum log value that will be kept "
                       "after the filter is applied. In the same units as the "
                       "y values for the sample log."},

                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs, 64")',
                         'data.keep_data_sample_log_between("Temp", 1.5, 2.7)',
                         'hist, bins = data.histogram()']),

            Doc('delete_sample_log_filter',
                'data.muon_data.MuonData',
                [MUONDATA, LOG, FILTER],
                "A method to delete a filter that "
                "acts upon sample logs from the "
                "MuonData object.",
                param={'name': 'The name of the sample log filter to remove. '
                       'Histograms need to be created to upate the data.'},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.keep_data_sample_log_between("Temp", 1.5, 2.7)',
                         'data.delete_sample_log_filter("Temp")',
                         'hist, bins = data.histogram()']),

            Doc('only_keep_data_time_between',
                'data.muon_data.MuonData',
                [MUONDATA, TIME, FILTER, HIST],
                "A method that only keeps complete frames from "
                "the specified time range, "
                "when creating histograms.",
                param={'name': 'A unique name to identify the filter.',
                       'start': 'The start time, in seconds, for the filter. '
                       'The filter is applied when creating a histogram.',
                       'end': 'The end time in seconds for the filter.'
                       'The filter is applied when creating a histogram.'},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.only_keep_data_time_between("Beam on", '
                         '5.8, 200.1)',
                         'hist, bins = data.histogram()']),

            Doc('delete_only_keep_data_time_between',
                'data.muon_data.MuonData',
                [MUONDATA, TIME, FILTER, HIST],
                "A method that removes the filter for "
                "keeping data within a specific time range, "
                "when creating a histograms.",
                param={'name': 'The name of the time filter to remove.'},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.only_keep_data_time_between("Beam on", '
                         '5.8, 200.1)',
                         'data.delte_only_keep_data_time_between(Beam on")']),

            Doc('remove_data_time_between',
                'data.muon_data.MuonData',
                [MUONDATA, TIME, FILTER, HIST],
                "A method to exclude data between two "
                "specified times from a MuonData "
                "object, when creating a histogram. "
                "If the filter only occupies part of the frame, "
                "the whole frame is discarded from the histogram genetation.",
                param={'name': 'A unique name to identify the filter.',
                       'start': 'The time to start removing data from, '
                       'in seconds.',
                       'end': "The last time to remove data from, in "
                       "seconds."},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.remove_data_time_between("Beam off", '
                         '11.3, 34.6)']),

            Doc('delete_remove_data_time_between',
                'data.muon_data.MuonData',
                [MUONDATA, TIME, FILTER, HIST],
                "A method to delete a filter "
                "from the MuonData object that "
                "removes data between two user "
                "defined times.",
                param={'name': "The name of the time filter to remove "
                       "when generating histograms"},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.remove_data_time_between("Beam off", '
                         '11.3, 34.6)',
                         'data.delete_remove_data_time_between("Beam off")']),

            Doc('get_frame_start_times',
                'data.muon_data.MuonData',
                [MUONDATA, TIME],
                "A method to get the list of frame "
                "start times in seconds from a "
                "MuonData object.",
                returns='A list of the frame start times in seconds. ',
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'start_times = data.get_frame_start_times()']),

            Doc('report_filters',
                'data.muon_data.MuonData',
                [MUONDATA, FILTER],
                "A method to return a Python "
                "dict of the filters that are "
                "currently active on the "
                "MuonData object.",
                returns='A structured dict of the current filters',
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'filters = data.report_filters()']),

            Doc('load_filters',
                'data.muon_data.MuonData',
                [MUONDATA, FILTER],
                "A method to read and add filters "
                "to a MuonData object from a JSON file.",
                param={'file_name': 'The name of the file, that '
                       'contains the filters '
                       "to be read and added to the MuonData object."},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.load_filters("example_filters.json")']),

            Doc('save_filters',
                'data.muon_data.MuonData',
                [MUONDATA, FILTER],
                "A method to save the current "
                "active filters from a MuonData "
                "object to a JSON file.",
                param={'file_name': "The name and path of the file "
                       "to save to a NeXu v2 file."},
                example=['from MuonDataLib.data.loader.load_events '
                         'import load_events',
                         'data = load_events("HIFI00001.nxs", 64)',
                         'data.only_keep_data_time_between("Beam on", '
                         '5.8, 200.1)',
                         'data.keep_sample_log_below("Temp", 5.2)',
                         'data.save_filters("example_filters.json")'])]
