from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.time.presenter import TimePresenter
from MuonDataLib.GUI.log.presenter import LogPresenter
from MuonDataLib.GUI.filters.view import FilterView
import numpy as np


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
        self._view = FilterView(self)
        self._data = None
        self._file_data = []

    def show_file(self, name, data):
        """
        If to display the name of the loaded
        filter file. This method chekcs
        the data currently in the table,
        so if you alter it and then change it
        back the file name will reappear.
        :param name: the name of the file
        :param data: the data from the file
        :returns: if to show the name in the GUI
        """
        if self._file_data == data:
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

    def apply_filters(self, time_filters, state, log_filters):
        """
        A method to apply the filters to the
        muon event data object. This allows
        for the user to state if the time
        window is included or excluded.
        :param time_filters: A list of filters (dicts)
        :param state: If to include or exclude the data
        """
        if len(time_filters) == 0 and len(log_filters) == 0:
            return
        elif state == 'Exclude':
            for filter_details in time_filters:
                self._data.remove_data_time_between(
                        filter_details['Name_time-table'],
                        filter_details['Start_time-table'],
                        filter_details['End_time-table'])
        else:
            for filter_details in time_filters:
                self._data.only_keep_data_time_between(
                        filter_details['Name_time-table'],
                        filter_details['Start_time-table'],
                        filter_details['End_time-table'])

        for filter_details in log_filters:

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

    def update_filters(self, time_filters, state, log_filters):
        # a bit heavyhanded, but guarantees that the filters can be applied
        self._data.clear_filters()
        if len(time_filters) == 0 and len(log_filters) == 0:
            return [], [], ''
        try:
            self.apply_filters(time_filters, state, log_filters)
        except RuntimeError as msg:
            return [], [], str(msg)
        start, stop = self._data.get_filters_as_times()
        return start, stop, ''

    def get_inc_filters(self, ex_start, ex_stop, row_log):
        log = self._log._logs.get_sample_log(row_log['sample_log-table'])
        x, y = log.get_original_values()

        f_start = [x[0]]
        f_stop = [ex_start[0]]

        f_start.append(ex_stop[0])
        for k in range(1, len(ex_stop)):
            f_stop.append(ex_start[1])
            f_start.append(ex_stop[1])

        f_stop.append(x[-1])

        print(f_start, ex_start)
        print(f_stop, ex_stop)
        return f_start, f_stop, np.min(y), np.max(y)

    def calculate(self, n_clicks, time_filters, state, log_filters):
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
        :returns: The string to display the number
        of events, the error message (if there is one)
        """
        self.update_filters(time_filters,
                            state,
                            log_filters)

        # a bit heavyhanded, but guarantees that the filters can be applied
        self._data.clear_filters()
        try:
            self.apply_filters(time_filters, state, log_filters)
        except RuntimeError as msg:
            return self._view.get_N(0), str(msg)
        _ = self._data.histogram()
        N = f"{self._data._cache.get_N_events:,}"
        return self._view.get_N(N), ''

    def load(self, filters):
        """
        Loads the filters that have been reported from a json file
        :param filters: the dict of the filters
        :returns: the filters and if to include/exclude
        """
        data, state = self._time.load(filters['time_filters'])
        self._file_data = data
        self._time.set_state(state)
        return data, state, self.headers

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
