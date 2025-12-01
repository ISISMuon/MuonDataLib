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
        """
        self._time = TimePresenter()
        self._view = FilterView(self)
        self._data = None

    def apply_filters(self, filters, state):

        if state == 'Exclude':
            for filter_details in filters:
                self._data.remove_data_time_between(
                        filter_details['Name_t'],
                        filter_details['Start_t'],
                        filter_details['End_t'])
        else:
            if len(filters)==0:
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
        """
        # a bit heavyhanded
        self._data.clear_filters()
        try:
            self.apply_filters(filters, state)
        except RuntimeError as msg:
            return self._view.get_N(0), str(msg)
        _ = self._data.histogram()
        return self._view.get_N(self._data._cache.get_N_events), ''

    def load(self, file):
        data, state = self._time.load(file['time_filters'])
        return data, state

    def update_N_events(self, update, current_str):
        if update:
            return self._view.no_events_str
        else:
            return current_str
