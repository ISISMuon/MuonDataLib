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

        # a copy of sample logs object
        self._logs = None
        # a list of default sample logs
        self._defaults = ['Temp_Sample']
        # number of time ok has been clicked in pop-up
        self._ok_clicks = 0
        # if we are replacing a sample log (if so which row)
        self._replace = None
        # the current name for the pop up
        self._selected_name = self._defaults[0]
        # create a plot area for pop up
        self._plot = PlotAreaPresenter('log')

        # create table
        name = Column('Name_' + LOG_TABLE, 'Name', 'text')

        log = Column('change_btn_' + LOG_TABLE, '', 'button')
        log.set_icon(icon='bi bi-graph-up me-2', class_name='btn btn-primary')

        sample = Column('sample_' + LOG_TABLE, 'selected', 'text')
        sample.set_uneditable()

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
        :returns: the log table view
        """
        return LogView(self)

    def set_logs(self, logs):
        """
        Sets the sample logs object
        :param logs: the sample logs object
        """
        self._logs = logs

    def btn_pressed(self, info, data):
        """
        It is not possible to differentiate between
        different buttons in the same table. So
        we use this method to identify which one was pressed
        and to do the correct response. The options are:
        - Open sample log pop up
        - delete row
        :param info: the information on the button pressed
        :param data: the data from the table
        :returns: the updated data and if to open the sample log pop up
        """
        if 'change_btn_log-table' == info['colId']:
            self._selected_name = data[info['rowIndex']]['sample_log-table']
            self._replace = info['rowIndex']
            return data, True
        else:
            return self.delete_row(info, data), False

    def get_available_logs(self, data):
        """
        We want to prevent the same sample log being selected
        multiple times. This method gets a list of unused sample
        logs. This also includes logic to keep a sample log
        if its being replaced by the user pressing the graph
        button in the table.
        :param data: the sample log table data (so we
        know which are in use)
        :returns: a list of the unused sample logs
        """
        # need to make a copy of the list so not to delete sample logs
        names = self._logs.get_names().copy()
        in_use = [row['sample_' + LOG_TABLE] for row in data]
        for taken in in_use:
            """
            If the user has pressed the graph button, the sample log
            is being replaced (not None value). Otherwise its a new row.
            If the sample log is being replaced/updated then we only want
            to keep the name of the one being replaced.
            """
            if self._replace is None or self._selected_name != taken:
                names.remove(taken)
        return names

    def get_new_log_name(self, data):
        """
        This gets the name of the next sample log,
        based on the default list and then just the
        first one that is not in use.
        :param data: the sample log table data
        :returns: the next name to be used
        """
        names = self.get_available_logs(data)
        for default in self._defaults:
            if default in names:
                return default
        return names[0]

    def show_log_data(self, name):
        """
        This method is to populate the sample log pop up with
        stats and a nice plot.
        :param name: name of the sample log to be displayed
        :returns: for the sample log (name) it will yield:
        - a plot of the data
        - the max y value
        - the mean y value
        - the min y value
        - the sigma (std)
        """
        _, y = self._logs.get_sample_log(name).get_original_values()

        return (self._plot.new_plot([name], self._logs),
                f'Max: {np.max(y):.3f}',
                f'Mean: {np.mean(y):.3f}',
                f'Min: {np.min(y):.3f}',
                f'Sigma (std): {np.std(y):.3f}')

    def select_log(self, is_open, data):
        """
        This method sets up the combo box for
        the pop up.
        :param is_open: if the pop up is open (not used)
        :param data: the sample log table data
        :returns: a list of names for the combo box and the
        selected value
        """
        options = self.get_available_logs(data)
        # if replacing/updating a row want to keep the name
        if self._replace is not None:
            return options, self._selected_name
        return options, self.get_new_log_name(data)

    def close_modal(self, ok, cancel, name, data):
        """
        A method for closing the pop up. To tell
        if ok or cancel has been pressed we track
        the number of ok presses. If ok is pressed
        we update the sample log table. If cancel is
        pressed we don't change the sample log table.
        :param ok: number of times ok has been pressed
        :param cancel: the number of times cancel has
        been pressed
        :param name: the name of the sample log being viewed
        (if ok is pressed it will be added/updated in the table)
        :param data: the sample log table data
        :returns if the pop up is open (always no) and
        the updated sample log table data.
        """
        del self._plot.fig
        self._plot.fig = None

        # was ok or cancel pressed?
        if self._ok_clicks < ok:
            # ok pressed
            if self._replace is not None:
                # replace/update row (i.e. graph button pressed)
                data[self._replace]['sample_log-table'] = name
            else:
                # new row (i.e. from add button)
                data.append(self.generate_default(data,
                                                  name))
            self._ok_clicks += 1

        return False, data

    def add(self, n, data):
        """
        Adds a row to the table.
        :param n: the number of clicks of the add button
        :param data: A list of the row data (as a dict)
        :returns: if the pop up should be opened (always yes)
        and the name of the selected sample log on opening
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
                self.name_col: 'log_' + self.get_next_row_name,
                'sample_log-table': name}
