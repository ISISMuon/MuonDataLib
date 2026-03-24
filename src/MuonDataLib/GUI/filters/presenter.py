from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.time.presenter import TimePresenter
from MuonDataLib.GUI.log.presenter import LogPresenter
from MuonDataLib.GUI.amp.presenter import AmpPresenter
from MuonDataLib.GUI.filters.view import FilterView


class FilterPresenter(PresenterTemplate):
    """
    A class for the filter widget's presenter.
    This code follows the MVP template,
    note that the model is MuonDataLib.
    """
    def __init__(self):
        """
        Create the presenter.
        Hold a copy of:
        - time filter table
        """
        self._time = TimePresenter()
        self._log = LogPresenter()
        self._amp = AmpPresenter()
        self._view = FilterView(self)
        self._data = None
        self._time_file_data = []
        self._log_file_data = []
        self._amp_file_data = 0

    def show_file(self, name, time_data, log_data, amp_data):
        """
        If to display the name of the loaded
        filter file. This method chekcs
        the data currently in the table,
        so if you alter it and then change it
        back the file name will reappear.
        :param name: the name of the file
        :param time_data: the data from the
        time filter table
        :param log_data: the log data for the
        log filter table
        :param amp_data: The amplitude filter data
        :returns: if the  the name in the GUI
        """
        if (self._time_file_data == time_data and
                self._log_file_data == log_data and
                self._amp_file_data == float(amp_data)):
            return False
        return True

    @property
    def headers(self):
        """
        Get the column headers
        :returns: the column headers (time table)
        """
        return self._time.cols.get_column_dict

    def set_data(self, data):
        """
        A method to set the muon data
        :param data: MuonEventData
        """
        self._data = data
        self._log.set_logs(data._dict['logs'])
        times = self._data.get_frame_start_times()

        self._time.set_time_range(times[0], times[-1] + 32e-6)

    def apply_filters(self, time_filters, state, log_filters, amp_filters):
        """
        A method to apply the filters to the
        muon event data object. This allows
        for the user to state if the time
        window is included or excluded.
        :param time_filters: A list of filters (dicts)
        :param state: If to include or exclude the data
        :param log_filters: a list of log filters
        :param amp_filters: amplitude filter
        """
        if (len(time_filters) == 0 and
                len(log_filters) == 0 and
                amp_filters == 0):
            # if no filters, do nothing
            return

        elif state == 'Exclude':
            # exclude time filters
            for filter_details in time_filters:
                self._data.remove_data_time_between(
                        filter_details['Name_time-table'],
                        filter_details['Start_time-table'],
                        filter_details['End_time-table'])
        else:
            # include time filters
            for filter_details in time_filters:
                self._data.only_keep_data_time_between(
                        filter_details['Name_time-table'],
                        filter_details['Start_time-table'],
                        filter_details['End_time-table'])

        for filter_details in log_filters:
            # loop over log filters
            filter_type = filter_details['filter_log-table']
            sample_log = filter_details['sample_log-table']
            start = filter_details['y0_log-table']
            stop = filter_details['yN_log-table']

            if filter_type == 'between':
                self._data.keep_data_sample_log_between(sample_log,
                                                        start,
                                                        stop)
            elif filter_type == 'above':
                self._data.keep_data_sample_log_above(sample_log,
                                                      start)
            elif filter_type == 'below':
                self._data.keep_data_sample_log_below(sample_log,
                                                      stop)
        self._data.keep_data_peak_property_above("Amplitudes",
                                                 float(amp_filters))

    def update_filters(self, time_filters, state, log_filters, amp_filters):
        """
        Gets the updated start and stop times for the
        exclude filters. The first step is a bit
        heavy handed, but it makes sure that we
        have no repeated names for the filters
        by clearning all of them.
        :param time_filters: the data from the time
        filter table
        :param state: the state (include or exclude)
        for the time filter table
        :param log_filters: the data from the sample
        log filter table
        :param apm_filters: the amplitude filter
        :returns: a list of the exclude filter start times,
        a list of the exclude filter end times,
        an error message.
        """
        self._data.clear_filters()
        if len(time_filters) == 0 and len(log_filters) == 0:
            return [], [], ''
        try:
            self.apply_filters(time_filters, state, log_filters, amp_filters)
        except RuntimeError as msg:
            return [], [], str(msg)
        start, stop = self._data.get_filters_as_times()
        return start, stop, ''

    def filters_rm_overlaps(self, ex_start, ex_end):
        """"
        This converts the exclude filter times
        into times for an inclusive filter. i.e.
        these are the inverse of each other.
        :param ex_start: the exclude start times
        :param ex_end: the exclude end times
        :returns: the start and end values
        to keep data between (include filter).
        """
        f_start = [ex_start[0]]
        f_end = []

        for j in range(len(ex_start)-1):
            if ex_start[j+1] > ex_end[j]:
                f_end.append(ex_end[j])
                f_start.append(ex_start[j+1])
        f_end.append(ex_end[-1])

        return f_start, f_end

    def get_log_y_range(self, row_log):
        """
        Gets the min and max y values according to
        the sample log filter table. e.g. if an above
        filter it will give the threshold from the
        table and the maximum y value.
        :param row_log: a row from the log filter
        table
        :returns: the smallest and largest y values for
        the filter
        """
        log = self._log._logs.get_sample_log(row_log['sample_log-table'])
        x, y = log.get_original_values()

        f_type = row_log['magic']
        if f_type == 'between':
            return row_log['y0_log-table'], row_log['yN_log-table']

        elif f_type == 'above':
            return row_log['y0_log-table'], row_log['y_max_log-table']

        elif f_type == 'below':
            return row_log['y_min_log-table'], row_log['yN_log-table']

        return row_log['y_min_log-table'], row_log['y_max_log-table']

    def calculate(self, n_clicks, time_filters, state,
                  log_filters, amp_filter):
        """
        A method to calculate the number of
        events that would be used to make
        the histogram.
        :param n_clicks: the number of button
        presses for the calculate button
        :param time_filters: the list of time
        filters
        :param state: If to include or exclude the
        data.
        :param log_filters: the data from the
        sample log filter table
        :param amp_filter: the amplitude filter
        :returns: The string to display the number
        of events, the error message (if there is one)
        """
        self._data.clear_filters()
        try:
            self.apply_filters(time_filters, state, log_filters, amp_filter)
        except RuntimeError as msg:
            return self._view.get_N(0), str(msg)
        _ = self._data.histogram()
        N = f"{self._data._cache.get_N_events:,}"
        return self._view.get_N(N), ''

    def load(self, filters):
        """
        Loads the filters that have been reported from a json file
        :param filters: the dict of the filters
        :returns: the time filters, the sample log
        filters, the amplitude filters, if to include/exclude the time filters,
        and the table headers
        """
        time_data, state = self._time.load(filters['time_filters'])
        self._time_file_data = time_data
        self._time.set_state(state)

        log_data = self._log.load(filters['sample_log_filters'])
        self._log_file_data = log_data

        self._amp_file_data = self._amp.load(filters['peak_property'])

        print('loading filters ....')
        return time_data, log_data, self._amp_file_data, state, self.headers

    def update_N_events(self, update, current_str):
        """
        A method to provide the correct string to display
        after an update occurs. We need to clear the
        number of events if the filters change.
        :param update: If an update hass occured and is valid
        :param current_str: the current string for the number
        of events
        :returns: the string to display for the number of
        events
        """
        if update:
            return self._view.no_events_str
        else:
            return current_str
