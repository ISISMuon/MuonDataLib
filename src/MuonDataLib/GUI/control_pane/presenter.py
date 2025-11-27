from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.filters.presenter import FilterPresenter
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter
from MuonDataLib.GUI.control_pane.view import ControlPaneView


import dash_bootstrap_components as dbc
from dash import dash_table
from dash import Input, Output, callback, State
from collections import Counter
from dash import no_update
import numpy as np


class ControlPanePresenter(PresenterTemplate):
    """
    A class for the view of the filter
    widget. This follows the MVP
    pattern.
    """
    def __init__(self):
        """
        This creates the view object for the
        widget. The responses to the callbacks
        will be in the presenter.
        """
        self._plot = PlotAreaPresenter()
        self._filter = FilterPresenter()
        self._view = ControlPaneView(self)

    def add_filter(self, data, fig):
        self._plot.fig.layout.shapes = []
        if len(data) == 0:
            self._plot.add_shaded_region(self._plot._min, self._plot._max)
            return self._plot.fig

        start = []
        end = []
        exc = False
        # add the filters back
        for filter_details in data:
            if filter_details['Type_t'] == 'Include':
                self._plot.add_inc_data(filter_details)
            else:
                exc = True
                tmp = self._filter._time.get_exc_data(filter_details)
                start.append(tmp[0])
                end.append(tmp[1])
        self.apply_exc_data(start, end)
        if not exc:
            self._plot.add_shaded_region(self._plot._min, self._plot._max)
        return self._plot.fig

    def apply_exc_data(self, start, end):
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

    def display_hover(self, data, filters):
        if data is None:
            return False, no_update, no_update
        pt = data['points'][0]
        bbox = pt['bbox']
        added = []
        removed = []
        for filter_details in filters:
            if filter_details['Type_t'] == 'Include' and filter_details['Start_t'] <= pt['x'] and filter_details['End_t'] >= pt['x']:
                added.append(filter_details['Name_t'])
            elif filter_details['Type_t'] == 'Exclude' and (filter_details['Start_t'] <= pt['x'] and filter_details['End_t'] >= pt['x']):
                removed.append(filter_details['Name_t'])

        txt = 'Keep data: '
        len_removed = len(removed)
        len_added = len(added)
        if len_removed > 0 and len_added == 0:
            txt += 'False. '
            txt += 'Removed by: '
            for name in removed:
                txt += name +', '

        elif len_removed==0 and len_added == 0:
            txt += 'True.'

        elif len_removed==0 and len_added > 0:
            txt += 'True. '
            txt += 'Kept by: '
            for name in added:
                txt += name +', '

        elif len_removed > 0 and len_added > 0:
            txt += 'True. '
            txt += 'Removed by: '
            for name in removed:
                txt += name +', '
            txt += '. But added back by: '
            for name in added:
                txt += name +', '

        children = self._view.hover_text(pt, txt)
        return True, bbox, children
