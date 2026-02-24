from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.filters.presenter import FilterPresenter
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter
from MuonDataLib.GUI.control_pane.view import ControlPaneView

from dash import no_update
import numpy as np
import json


class ControlPanePresenter(PresenterTemplate):
    """
    The control pane contains the
    filters and the plot area.
    This is the presenter for the
    widget. This follows the MVP
    pattern.
    """
    def __init__(self):
        """
        This creates the presenter object for the
        widget.
        """
        self._plot = PlotAreaPresenter('main')
        self._filter = FilterPresenter()
        self._view = ControlPaneView(self)

    def plot_default(self):
        name = self._filter._log.get_new_log_name([])
        return self._plot.new_plot([name], self._filter._log._logs)

    def make_plot(self, time_data, log_data, state):
        """
        This methods adds filters to the plot.
        A filter is represented by removing the shaded
        region from the plot. i.e. only the shaded
        data is used in calculations.
        :param data: the data from the filter table
        :param state: if the filter is an exclude or include
        :returns: an updated figure
        """
        names = [row['sample_log-table'] for row in log_data]
        if len(names) == 0:
            names = [self._filter._log.get_new_log_name([])]
        self._plot.new_plot(names, self._filter._log._logs)
        return self.add_time_filters(time_data, state)

    def add_time_filters(self, time_data, state):
        if len(time_data) == 0 and state == 'Exclude':
            self._plot.add_shaded_region(self._plot._min, self._plot._max)
            return self._plot.fig

        start = []
        end = []
        # add the filters back
        if state == 'Include':
            for filter_details in time_data:
                span = self._filter._time.get_range(filter_details)
                self._plot.add_shaded_region(*span)
        else:
            for filter_details in time_data:
                tmp = self._filter._time.get_range(filter_details)
                start.append(tmp[0])
                end.append(tmp[1])
            self.apply_exc_data(start, end)
        return self._plot.fig

    def apply_exc_data(self, start, end):
        """
        Applys the exclusion of data from
        the analysis. i.e. the area is not
        shaded.
        :param start: A list of start values
        for the exluded regions
        :param end: A list of end values
        for the excluded regions
        """
        if len(start) == 0:
            return

        sorted_start = np.sort(start)
        sorted_end = np.sort(end)

        f_start = [sorted_start[0]]
        f_end = []

        for j in range(len(sorted_start)-1):
            if sorted_start[j+1] > sorted_end[j]:
                f_end.append(sorted_end[j])
                f_start.append(sorted_start[j+1])
        f_end.append(sorted_end[-1])

        self._plot.add_shaded_region(self._plot._min, f_start[0])
        for j in range(1, len(f_start)):
            self._plot.add_shaded_region(f_end[j-1], f_start[j])

        self._plot.add_shaded_region(f_end[-1], self._plot._max)

    def set_data(self, data):
        """
        A simple setter for the MuonEventData
        Will also reset the range for the plot
        :param data: MuonEventData
        """
        self._plot.reset_plot_range()
        self._filter.set_data(data)

    @property
    def headers(self):
        """
        :returns: the column headers
        """
        return self._filter.headers

    def display_hover(self, hover_info, filters, state):
        """
        A method for getting the hover text
        for the plot. This will say if data is
        being used in the analysis or not and
        which filters add/remove it.
        :param hover_info: the hover data
        :param filters: the time filters
        :param state: if the filter is an exclude or include
        :returns: if to show tooltip text, the bounding box for the tooltip
        and the text for the tooltip
        """
        if hover_info is None:
            return False, no_update, no_update
        pt = hover_info['points'][0]
        bbox = pt['bbox']
        added = []
        removed = []
        txt = 'Keep data: '

        if state == 'Include':
            for filter_details in filters:
                start, end = self._filter._time.get_range(filter_details)
                if start <= pt['x'] and end >= pt['x']:
                    added.append(filter_details['Name_time-table'])
            if len(added) > 0:
                txt += 'True. '
                txt += 'Added by: '
                for name in added:
                    txt += name + ', '
            else:
                txt += 'False'

        else:
            for filter_details in filters:
                start, end = self._filter._time.get_range(filter_details)
                if (start <= pt['x'] and end >= pt['x']):
                    removed.append(filter_details['Name_time-table'])
            if len(removed) > 0:
                txt += 'False. '
                txt += 'Removed by: '
                for name in removed:
                    txt += name + ', '
            else:
                txt += 'True'

        children = self._view.hover_text(pt, txt)
        return True, bbox, children

    def read_filter(self, name):
        """
        A method to get the filters from a file
        and populate the GUI.
        :param name: the name of the json file
        :returns: the data, the state for the time filter (include/exclude)
        and the column headers
        """
        with open(name, 'r') as file:
            data = json.load(file)
        data, state, cols = self._filter.load(data)
        return data, state, cols
