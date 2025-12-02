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

    def apply_filters(self, filters, state):
        """
        A method to apply the filters to the
        muon event data object. This allows
        for the user to state if the time
        window is included or excluded.
        :param filters: A list of filters (dicts)
        :param state: If to include or exclude the data
        """
        if state == 'Exclude':
            for filter_details in filters:
                self._data.remove_data_time_between(
                        filter_details['Name_t'],
                        filter_details['Start_t'],
                        filter_details['End_t'])
        else:
            if len(filters) == 0:
                raise RuntimeError('No data selected')
            for filter_details in filters:
                self._data.only_keep_data_time_between(
                        filter_details['Name_t'],
                        filter_details['Start_t'],
                        filter_details['End_t'])

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
        return self._view.get_N(self._data._cache.get_N_events), ''

    def load(self, filters):
        """
        Loads the filters from a json file
        :param filters: the dict of the filters
        """
        data, state = self._time.load(filters['time_filters'])
        return data, state

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
