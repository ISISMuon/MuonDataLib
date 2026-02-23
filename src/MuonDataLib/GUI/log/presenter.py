from MuonDataLib.GUI.table.presenter import TablePresenter
from MuonDataLib.GUI.log.view import LogView
from MuonDataLib.GUI.table.column import Column, TableGroup, TableColumns
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter


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
        # create columns
        name = Column('Name_' + LOG_TABLE, 'Name', 'text')
        log = Column('change_btn_' + LOG_TABLE, '', 'button')
        log.set_icon(icon='bi bi-graph-up me-2', class_name='btn btn-primary')
        sample = Column('sample_' + LOG_TABLE, 'selected', 'text')

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

    def select(self, name, log):

        return self._plot.new_plot([], log)
        # return self._plot.new_plot([name], log)

    def close_modal(self, a, b):
        del self._plot.fig
        self._plot.fig = None

    def add(self, n, data):
        """
        Adds a row to the table.
        :param n: the number of clicks of the add button
        :param data: A list of the row data (as a dict)
        :returns: the data for the table and if its valid
        """
        if not isinstance(data, list):
            data = []
        data.append(self.generate_default(data))
        return data

    def generate_default(self, data):
        """
        Code to create some default values
        :returns: a default dict
        """
        return {'Delete_' + self.ID: '',
                self.name_col: self.get_next_row_name,
                **self.default_row(data)}

    def default_row(self, data):
        """
        The code needed to create a default
        row for the time table
        :returns: dict of the values for the time table.
        """
        # names = self.logs.
        return {'sample_log-table': 'Temp_Sample'}
