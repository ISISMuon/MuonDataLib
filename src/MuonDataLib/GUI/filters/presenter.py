from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.time.presenter import TimePresenter
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
        self._view = FilterView(self)
        self._data = None
        self._file_data = []

    def show_file(self, name, data):
        if self._file_data == data:
            self._file = name
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
        times = self._data.get_frame_start_times()

        self._time.set_time_range(times[0], times[-1] + 32e-6)

    def apply_filters(self, filters, state):
        """
        A method to apply the filters to the
        muon event data object. This allows
        for the user to state if the time
        window is included or excluded.
        :param filters: A list of filters (dicts)
        :param state: If to include or exclude the data
        """
        if len(filters) == 0:
            return
        elif state == 'Exclude':
            for filter_details in filters:
                self._data.remove_data_time_between(
                        filter_details['Name_time-table'],
                        filter_details['Start_time-table'],
                        filter_details['End_time-table'])
        else:
            for filter_details in filters:
                self._data.only_keep_data_time_between(
                        filter_details['Name_time-table'],
                        filter_details['Start_time-table'],
                        filter_details['End_time-table'])

    def calculate(self, n_clicks, filters, state):
        """
        A method to calculate the number of
        events that would be used to make
        the histogram.
        :param n_clicks: the number of button
        presses for the calculate button
        :param filters: the list of time
        filters
        :param state: If to include or exclude the
        data.
        :returns: The string to display the number
        of events, the error message (if there is one)
        """
        # a bit heavyhanded, but guarantees that the filters can be applied
        self._data.clear_filters()
        try:
            self.apply_filters(filters, state)
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
