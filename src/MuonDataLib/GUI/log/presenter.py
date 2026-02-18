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

    def select(self, state):
        return self._plot.plot([1, 2, 3, 4],
                               [1, 2, 3, 4],
                               [11, 12, 24],
                               [7, 3, 1])

    @property
    def default_row(self):
        """
        The code needed to create a default
        row for the time table
        :returns: dict of the values for the time table.
        """
        return {}
