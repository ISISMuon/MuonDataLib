from MuonDataLib.GUI.table.presenter import TablePresenter
from MuonDataLib.GUI.log.view import LogView
from MuonDataLib.GUI.table.column import Column, TableGroup, TableColumns
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter
import numpy as np


LOG_TABLE = 'log-table'


class LogPresenter(TablePresenter):
    """
    A class for the view of the sample log filter
    widget. This follows the MVP
    pattern.
    """
    def __init__(self):
        """
        This creates the presenter object for the
        widget.
        """
        self._logs = None
        self._defaults = ['Temp_Sample']
        self._ok_clicks = 0
        self._replace = None
        self._selected_name = self._defaults[0]
        # create columns
        name = Column('Name_' + LOG_TABLE, 'Name', 'text')
        log = Column('change_btn_' + LOG_TABLE, '', 'button')
        log.set_icon(icon='bi bi-graph-up me-2', class_name='btn btn-primary')
        sample = Column('sample_' + LOG_TABLE, 'selected', 'text')
        sample.set_uneditable()

        self._plot = PlotAreaPresenter('log')

        cols = TableColumns([TableGroup([name]),
                             TableGroup([log, sample], 'Sample logs')],
                            inc_delete_row=True,
                            btn_ID=LOG_TABLE)

        super().__init__(LOG_TABLE,
                         cols,
                         name.ID)

    def _set_view(self):
        """
        Overwrite the view to give a time table view
        """
        return LogView(self)

    def set_logs(self, logs):
        self._logs = logs

    def btn_pressed(self, info, data):
        if 'change_btn_log-table' == info['colId']:
            self._selected_name = data[info['rowIndex']]['sample_log-table']
            self._replace = info['rowIndex']
            return data, True
        else:
            return self.delete_row(info, data), False

    def get_available_logs(self, data):
        names = self._logs.get_names().copy()
        in_use = [row['sample_' + LOG_TABLE] for row in data]
        for taken in in_use:
            if self._replace is None or self._selected_name != taken:
                names.remove(taken)
        return names

    def get_new_log_name(self, data):
        names = self.get_available_logs(data)
        for default in self._defaults:
            if default in names:
                return default
        return names[0]

    def show_log_data(self, name):
        _, y = self._logs.get_sample_log(name).get_original_values()

        return (self._plot.new_plot([name], self._logs),
                f'Max: {np.max(y):.3f}',
                f'Mean: {np.mean(y):.3f}',
                f'Min: {np.min(y):.3f}',
                f'Sigma (std): {np.std(y):.3f}')

    def select_log(self, state, data):
        options = self.get_available_logs(data)
        if self._replace is not None:
            return options, self._selected_name
        return options, self.get_new_log_name(data)

    def close_modal(self, ok, cancel, name, data):
        del self._plot.fig
        self._plot.fig = None
        # otherwise assume cancel pressed
        if self._ok_clicks < ok:
            if self._replace is not None:
                data[self._replace]['sample_log-table'] = name
            else:
                data.append(self.generate_default(data,
                                                  name))
            self._ok_clicks += 1
        return False, data

    def add(self, n, data):
        """
        Adds a row to the table.
        :param n: the number of clicks of the add button
        :param data: A list of the row data (as a dict)
        :returns: the data for the table and if its valid
        """
        self._replace = None
        self._selected_name = self.get_new_log_name(data)
        return True, self.get_new_log_name(data)

    def generate_default(self, data, name):
        """
        Code to create some default values
        :returns: a default dict
        """
        return {'Delete_' + self.ID: '',
                self.name_col: self.get_next_row_name,
                'sample_log-table': name}
