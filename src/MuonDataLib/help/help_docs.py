class Doc(object):
    def __init__(self, name, module, tags, description=''):
        # param, optional_param, returns):
        self.name = name
        self.module = module
        self.tags = tags
        self.description = description
        # self.param = param
        # self.optional_param = optional_param
        # self.returns = returns

    def get_MD(self):
        text = f'''
                # {self.module}.{self.name}

                ### Module: {self.module}

                {self.description}


                '''
        return text


_text = [Doc('MuonData',
             'data.muon_data',
             ['MuonData'],
             "An object that stores the relevant information "
             "for muon data (as definied by NeXus version 2)"),
         Doc('save_histograms',
             'data.muon_data',
             ['MuonData', 'histograms', 'NeXus'],
             "Method for saving a MuonData object to a "
             "NeXus v2 histogram file "
             "This will skip calculating the filters "
             "if the cache is occupied. "
             "If just the resolution has changed it will "
             "not alter the filtered values."),
         Doc('histogram',
             'data.muon_data',
             ['MuonData', 'histograms'],
             "A method for constructing a histogram from a MuonData object. "
             "This method is helpful for checking results. "
             "This will skip calculating the filters "
             "if the cache is occupied. "
             "If just the resolution has changed it will "
             "not alter the filtered values."),
         Doc('clear_filters',
             'data.muon_data',
             ['MuonData', 'filter', 'time', 'sample log'],
             "A method to remove all of the filters from the "
             "MuonData object."),
         Doc('add_sample_log',
             'data.muon_data',
             ['MuonData', 'sample log'],
             "A method to manually add a sample log to a MuonData object."),
         Doc('get_sample_log',
             'data.muon_data',
             ['MuonData', 'sample log', 'LogData'],
             "A method to get a specific sample log (LogData object) "
             "from a MuonData object."),
         Doc('keep_data_sample_log_below',
             'data.muon_data',
             ['MuonData', 'sample log', 'filter', 'histograms'],
             "A method to remove all frames containing data "
             "with a value above some threshold value for a "
             "specific sample log, "
             "when creating a histogram from a MuonData object."),
         Doc('keep_data_sample_log_above',
             'data.muon_data',
             ['MuonData', 'sample log', 'filter', 'histograms'],
             "A method to remove all frames containing data "
             "with a value below some threshold value for a "
             "specific sample log, "
             "when creating a histogram from a MuonData object."
             ),
         Doc('keep_data_sample_log_between',
             'data.muon_data',
             ['MuonData', 'sample log', 'filter', 'histograms'],
             "A method to only keep frames containing data "
             "between a pair of values for a specific sample log, "
             "when creating a histogram from a MuonData object."
             ),
         Doc('only_keep_data_time_between',
             'data.muon_data',
             ['MuonData', 'time', 'filter', 'histograms'],
             "A method that only keeps complete frames from "
             "the specified time range, "
             "when creating a histograms."),
         Doc('delete_only_keep_data_time_between',
             'data.muon_data',
             ['MuonData', 'time', 'filter', 'histograms'],
             "A method that removes the filter for "
             "keeping data within a specific time range, "
             "when creating a histograms."
             ),
         Doc('remove_data_time_between',
             'data.muon_data',
             ['MuonData', 'time', 'filter']),
         Doc('delete_remove_data_time_between',
             'data.muon_data',
             ['MuonData', 'time', 'filter']),
         Doc('delete_sample_log_filter',
             'data.muon_data',
             ['MuonData', 'sample log', 'filter']),
         Doc('get_frame_start_times',
             'data.muon_data',
             ['MuonData', 'time']),
         Doc('report_filters',
             'data.muon_data',
             ['MuonData', 'filter']),
         Doc('load_filters',
             'data.muon_data',
             ['MuonData', 'filter']),
         Doc('save_filters',
             'data.muon_data',
             ['MuonData', 'filter']),

         Doc('load_events',
             'data.loader.load_events',
             ['load_events', 'NeXus', 'MuonData']),

         Doc('Figure',
             'plot.basic',
             ['plotting']),
         Doc('plot',
             'plot.basic',
             ['plotting']),
         Doc('show',
             'plot.basic',
             ['plotting']),
         Doc('plot_from_histogram',
             'plot.basic',
             ['plotting', 'histograms']),
         Doc('plot_from_histogram',
             'plot.basic',
             ['plotting', 'sample log', 'MuonData'])
         ]
tags = []
for method in _text:
    names = method.tags
    for val in names:
        if val not in tags:
            tags.append(val)
tags = sorted(tags)
