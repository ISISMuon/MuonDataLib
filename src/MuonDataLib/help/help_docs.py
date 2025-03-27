class Doc(object):
    def __init__(self, name, module, tags, description='',
                 param='', optional_param='', returns='',
                 example=''):
        self.name = name
        self.module = module
        self.tags = tags
        self.description = description
        self.param = param
        self.optional_param = optional_param
        self.returns = returns
        self.example = example

    def get_MD(self):
        text = f'''
                # `{self.module}`.{self.name}

                {self.description} \n\n'''

        space = '''                '''

        if len(self.param) > 0:
            tmp = space + '''**Required Parameters:** \n'''
            for info in self.param.keys():
                tmp += space + f'''- `{info}`: {self.param[info]} \n '''
            text += tmp

        if self.optional_param != '':
            tmp = space + '''**Required Parameters:** \n'''
            for info in self.optional_param:
                tmp += space + f'''- {info} \n '''
            text += tmp

        if self.returns != '':
            text += '''\n''' + space + f'''**Returns:** {self.returns} \n'''

        if len(self.example) > 0:
            text += "\n" + space + """**Example:** \n"""
            text += space + """``` python \n"""
            for eg in self.example:
                text += space + f'''{eg} \n'''
            text += space + """```"""
            print(text)
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
             example=['from MuonDataLib.data.muon_data import MuonData',
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
             "not alter the filtered values."),
         Doc('histogram',
             'data.muon_data.MuonData',
             ['MuonData', 'histograms'],
             "A method for constructing a histogram from a MuonData object. "
             "This method is helpful for checking results. "
             "This will skip calculating the filters "
             "if the cache is occupied. "
             "If just the resolution has changed it will "
             "not alter the filtered values."),
         Doc('clear_filters',
             'data.muon_data.MuonData',
             ['MuonData', 'filter', 'time', 'sample log'],
             "A method to remove all of the filters from the "
             "MuonData object."),
         Doc('add_sample_log',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log'],
             "A method to manually add a sample log to a MuonData object."),
         Doc('get_sample_log',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log', 'LogData'],
             "A method to get a specific sample log (LogData object) "
             "from a MuonData object."),
         Doc('keep_data_sample_log_below',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log', 'filter', 'histograms'],
             "A method to remove all frames containing data "
             "with a value above some threshold value for a "
             "specific sample log, "
             "when creating a histogram from a MuonData object."),
         Doc('keep_data_sample_log_above',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log', 'filter', 'histograms'],
             "A method to remove all frames containing data "
             "with a value below some threshold value for a "
             "specific sample log, "
             "when creating a histogram from a MuonData object."
             ),
         Doc('keep_data_sample_log_between',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log', 'filter', 'histograms'],
             "A method to only keep frames containing data "
             "between a pair of values for a specific sample log, "
             "when creating a histogram from a MuonData object."
             ),
         Doc('only_keep_data_time_between',
             'data.muon_data.MuonData',
             ['MuonData', 'time', 'filter', 'histograms'],
             "A method that only keeps complete frames from "
             "the specified time range, "
             "when creating a histograms."),
         Doc('delete_only_keep_data_time_between',
             'data.muon_data.MuonData',
             ['MuonData', 'time', 'filter', 'histograms'],
             "A method that removes the filter for "
             "keeping data within a specific time range, "
             "when creating a histograms."
             ),
         Doc('remove_data_time_between',
             'data.muon_data.MuonData',
             ['MuonData', 'time', 'filter'],
             "A method to exclude data between two "
             "specified times from a MuonData "
             "object, when creating a histogram."),

         Doc('delete_remove_data_time_between',
             'data.muon_data.MuonData',
             ['MuonData', 'time', 'filter'],
             "A method to delete a filter "
             "from the MuonData object that "
             "removes data between two user "
             "defined times."),

         Doc('delete_sample_log_filter',
             'data.muon_data.MuonData',
             ['MuonData', 'sample log', 'filter'],
             "A method to delete a filter that "
             "acts upon sample logs from the "
             "MuonData object."),

         Doc('get_frame_start_times',
             'data.muon_data.MuonData',
             ['MuonData', 'time'],
             "A method to get the list of frame "
             "start times in seconds from a "
             "MuonData object."),

         Doc('report_filters',
             'data.muon_data.MuonData',
             ['MuonData', 'filter'],
             "A method to return a Python "
             "dict of the filters that are "
             "currently active on the "
             "MuonData object."),

         Doc('load_filters',
             'data.muon_data.MuonData',
             ['MuonData', 'filter'],
             "A method to read and add filters "
             "to a MuonData object from a JSON file."),

         Doc('save_filters',
             'data.muon_data.MuonData',
             ['MuonData', 'filter'],
             "A method to save the current "
             "active filters from a MuonData "
             "object to a JSON file."),

         # load
         Doc('load_events',
             'data.loader.load_events',
             ['load_events', 'NeXus', 'MuonData'],
             "A method to load a muon event NeXus file "
             "into a MuonData object"),

         # figure
         Doc('Figure',
             'plot.basic',
             ['plotting'],
             "An object to handle making Plotly plots."),

         Doc('plot',
             'plot.basic.Figure',
             ['plotting'],
             "A method to create a simple plot in the "
             "Figure object."),

         Doc('show',
             'plot.basic.Figure',
             ['plotting'],
             "A method to generate and present the plot "
             "from the Figure object."),

         Doc('plot_from_histogram',
             'plot.basic.Figure',
             ['plotting', 'histograms'],
             "A method to store that data needed "
             "to make a plot of histogram data."),

         Doc('plot_from_sample_log',
             'plot.basic.Figure',
             ['plotting', 'sample log', 'MuonData'],
             "A method to add the data to plot "
             "the current (filtered) sample logs "
             "and their original values.")
         ]
tags = []
for method in _text:
    names = method.tags
    for val in names:
        if val not in tags:
            tags.append(val)
tags = sorted(tags)
