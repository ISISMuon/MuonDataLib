class Doc(object):
    def __init__(self, name, module, tags, description='',
                 param={}, optional_param={}, returns='',
                 example=[]):
        self.name = name
        self.module = module
        self.tags = tags
        self.description = description
        self.param = param
        self.optional_param = optional_param
        self.returns = returns
        self.example = example

    def write_MD(self, file_name):
        text = self.get_MD()
        with open(file_name, 'a') as file:
            file.write(text)

    def get_MD(self):
        text = f'''# `{self.module}`.**{self.name}** \n'''
        text += f'''{self.description} \n\n'''

        space = ''

        if len(self.param) > 0:
            tmp = space + '''**Required Parameters:** \n'''
            for info in self.param.keys():
                tmp += space + f'''- `{info}`: {self.param[info]} \n '''
            text += tmp

        if len(self.optional_param) > 0:
            tmp = '''\n''' + space + '''**Optional Parameters:** \n'''
            for info in self.optional_param.keys():
                msg = self.optional_param[info]
                value = f'''- `{info}`: {msg[0]} *Default value:* `{msg[1]}`'''
                tmp += space + value + '''.\n '''
            text += tmp

        if self.returns != '':
            text += '''\n''' + space + f'''**Returns:** {self.returns} \n'''

        if len(self.example) > 0:
            text += "\n" + space + """**Example:** \n"""
            text += space + """``` python \n"""
            for eg in self.example:
                text += space + f'''{eg} \n'''
            text += space + """```"""
        return text


_text = [Doc('MuonData',
             'data.muon_data',
             ['MuonData'],
             "An object that stores the relevant information "
             "for muon data (as definied by NeXus version 2)."
             "This is automatically created by `load_events`.",
             {"sample": "The sample data.",
              "raw_data": "The raw data (as defined by NeXus group).",
              "source": "The source data (as defined by NeXus group).",
              "periods": "The period data (as defined by NeXus group).",
              "detector1": "The detector 1 data (as defined by NeXus group)."},
             returns="MuonData object.",
             example=['from MuonDataLib.data.muon_data '
                      'import MuonData',
                      'sample. raw, src, period, det = get_data()',
                      'muon = MuonData(sample, raw, src, period, det)']),

         Doc('save_histograms',
             'data.muon_data.MuonData',
             ['MuonData', 'histograms', 'NeXus'],
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
             ['MuonData', 'histograms'],
             "A method for constructing a histogram from a MuonData object. "
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
             ['MuonData', 'filter', 'time', 'sample log'],
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
             ['MuonData', 'sample log'],
             "A method to manually add a sample log to a MuonData object.",
             {'name': 'The name of the sample log.',
              'x_data': 'The x values for the sample log (time in seconds).',
              'y_data': 'The y values for the sample log'},
             example=['from MuonDataLib.data.loader.load_events '
                      'import load_events',
                      'import numpy as np',
                      'data = load_events("HIFI00001.nxs"), 64',
                      'x_data, y_data = np.load("Temp.txt")',
                      'data.add_sample_log("Temp", x_data, y_data)']),

         Doc('keep_data_sample_log_below',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log', 'filter', 'histograms'],
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
             ['MuonData', 'sample log', 'filter', 'histograms'],
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
             ['MuonData', 'sample log', 'filter', 'histograms'],
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
             ['MuonData', 'sample log', 'filter'],
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
             ['MuonData', 'time', 'filter', 'histograms'],
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
             ['MuonData', 'time', 'filter', 'histograms'],
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
             ['MuonData', 'time', 'filter'],
             "A method to exclude data between two "
             "specified times from a MuonData "
             "object, when creating a histogram. "
             "If the filter only occupies part of the frame, "
             "the whole frame is discarded from the histogram genetation.",
             param={'name': 'A unique name to identify the filter.',
                    'start': 'The time to start removing data from, '
                    'in seconds.',
                    'end': "The last time to remove data from, in seconds."},
             example=['from MuonDataLib.data.loader.load_events '
                      'import load_events',
                      'data = load_events("HIFI00001.nxs", 64)',
                      'data.remove_data_time_between("Beam off", '
                      '11.3, 34.6)']),

         Doc('delete_remove_data_time_between',
             'data.muon_data.MuonData',
             ['MuonData', 'time', 'filter'],
             "A method to delete a filter "
             "from the MuonData object that "
             "removes data between two user "
             "defined times.",
             param={'name': "The name of the time filter to remove "
                    "when generating histograms"},
             example=['from MuonDataLib.data.loader.load_events '
                      'import load_events',
                      'data = load_events("HIFI00001.nxs", 64)',
                      'data.remove_data_time_between("Beam off", 11.3, 34.6)',
                      'data.delete_remove_data_time_between("Beam off")']),

         Doc('get_frame_start_times',
             'data.muon_data.MuonData',
             ['MuonData', 'time'],
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
             ['MuonData', 'filter'],
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
             ['MuonData', 'filter'],
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
             ['MuonData', 'filter'],
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
                      'data.save_filters("example_filters.json")']),

         # load
         Doc('load_events',
             'data.loader.load_events',
             ['load_events', 'NeXus', 'MuonData'],
             "A method to load a muon event NeXus file "
             "into a MuonData object",
             param={'file_name': "The name of the event NeXus file to read.",
                    "N": "The number of expected spectra for the file."},
             example=['from MuonDataLib.data.loader.load_events import '
                      'load_events',
                      'data = load_events("HIFI00001.nxs", 64)']),

         # figure
         Doc('Figure',
             'plot.basic',
             ['plotting', 'Figure'],
             "An object to handle making Plotly plots.",
             optional_param={'title': ["The title for the plot.",
                                       ""],
                             'x_label': ['The label for the x axis.',
                                         'time (micro seconds)'],
                             'y_label': ['The label for the y axis.',
                                         'Counts']},
             example=['from MuonDataLib.plot.basic import Figure',
                      'fig = Figure("Example plot", '
                      'y_label="Temp (Kelvin)")']),

         Doc('plot',
             'plot.basic.Figure',
             ['plotting', 'Figure'],
             "A method to create a simple plot in the "
             "Figure object.",
             param={'bin_centres': 'The list of bin centres '
                    '(i.e. point data).',
                    'y_values': "The y values to plot.",
                    'label': 'The label to give the data set in the legend'},
             example=['from MuonDataLib.plot.basic import Figure',
                      'import numpy as np',
                      'fig = Figure("Example plot")',
                      'x = np.arange(0, 10)',
                      'y = np.sin(2.1*x)',
                      'fig.plot(x, y, "sin(2.1 x)")']),

         Doc('show',
             'plot.basic.Figure',
             ['plotting', 'Figure'],
             "A method to generate and present the plot "
             "from the Figure object.",
             example=['from MuonDataLib.plot.basic import Figure',
                      'import numpy as np',
                      'fig = Figure("Example plot")',
                      'x = np.arange(0, 10)',
                      'y = np.sin(2.1*x)',
                      'fig.plot(x, y, "sin(2.1 x)")',
                      'fig.show()']),

         Doc('plot_from_histogram',
             'plot.basic.Figure',
             ['plotting', 'Figure', 'histograms'],
             "A method to store that data needed "
             "to make a plot of histogram data.",
             param={'bins': 'The bin edges for the histogram.',
                    'hist': 'The histogram matrix (period, '
                    'spectrum number, bins).',
                    'det_list': 'The list of spectrum numbers to plot.'},
             optional_param={'label': ['The base label to use '
                                       'in the legend.', '""'],
                             'period': ['The period to plot.', '1']},
             example=['from MuonDataLib.plot.basic import Figure',
                      'from MuonDataLib.data.loader.load_events '
                      'import load_events',
                      'data = load_events("HIFI00001.nxs", 64)',
                      'hist, bins = data.histogram()',
                      'fig = Figure("Example plot")',
                      'fig.plot_from_histogram(bins, hist, [1, 3, 5], '
                      'label="HIFI00001")',
                      'fig.show()']),

         Doc('plot_sample_log',
             'plot.basic.Figure',
             ['plotting', 'Figure', 'sample log', 'MuonData'],
             "A method to add the data to plot "
             "the current (filtered) sample logs "
             "and their original values.",
             param={'muon_data': 'The MuonData object that contains '
                    'the log that we want to plot.',
                    'log_name': "The name of the sample log to plot"},
             example=['from MuonDataLib.plot.basic import Figure',
                      'from MuonDataLib.data.loader.load_events '
                      'import load_events',
                      'data = load_events("HIFI00001.nxs", 64)',
                      'fig = Figure("Example plot")',
                      'fig.plot_sample_log(data, "HIFI_field")',
                      'fig.show()']),
         # utils
         Doc('create_data_from_function',
             'data.utils',
             ['sample log', 'MuonData', 'utils'],
             "A method to create some fake data. "
             "It takes a function, its parameters and the x range "
             "to generate some fake data with noise in both x and y.",
             param={'x1': 'The start x value.',
                    'x2': 'The end x value.',
                    'dx': 'The average step size for the x data.',
                    'params': 'A list of the parameters to use '
                    'in the function',
                    'function': 'The callable function to use when '
                    'creating the data.'},
             optional_param={'seed': ['The seed value for the random '
                                      'number generator',
                                      'None']},
             returns='The fake x and y values.',
             example=['from MuonDataLib.data.loader.load_events '
                      'import load_events',
                      'from MuonDataLib.data.utils import '
                      'create_data_from_function',
                      'data = load_events("HIFI00001.nxs", 64)',
                      'times = data.get_frame_start_times()',
                      'N = 100', '',
                      'def linear(x, m c):',
                      '    return m*x + c', '',
                      'x, y = create_data_from_function(times[0], times[1], '
                      '(times[-1] - times[0])/N, [1.2, -2.1], linear, seed=1)',
                      'data.add_sample_log("Fake log", x, y)'])]
tags = []
for method in _text:
    names = method.tags
    for val in names:
        if val not in tags:
            tags.append(val)
tags = sorted(tags)
