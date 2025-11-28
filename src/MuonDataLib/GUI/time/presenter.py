from MuonDataLib.GUI.table.presenter import TablePresenter
from MuonDataLib.GUI.time.view import TimeView
from MuonDataLib.GUI.table.header import Header
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import Input, Output, callback, State
from collections import Counter


class TimePresenter(TablePresenter):
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
        self.count = 0

        self._previous = 'Exclude'
        name = Header('Name_t', ['', 'Name'])

        start = Header('Start_t', ['Exclude data', 'Start'])
        start.add_type('numeric')

        end = Header('End_t', ['Exclude data', 'End'])
        end.add_type('numeric')

        super().__init__('time-table',
                         [name, start, end],
                         name.ID)

    def _set_view(self):
        return TimeView(self)

    def validate_row(self, new_row, old_row):
        if new_row['Start_t'] > new_row['End_t']:
            return False, f'Start time {new_row["Start_t"]} is greater than end time {new_row["End_t"]}'
        return True, ''

    @property
    def generate_default(self):
        self.count += 1
        return {'Name_t': f'default_{self.count}',
                'Start_t': 500,
                'End_t': 1000}

    def get_exc_data(self, data):
        return [data['Start_t'], data['End_t']]

    def display_confirm(self, value, data):
        if len(data) == 0:
            return False
        elif self._previous != value:
            return True
        return False

    def confirm(self, submit, cancel, value, data):
        if submit > cancel:
            for k in range(len(self.cols)):
                header = self.cols[k]
                for key in header.keys():
                    if isinstance(header[key], list):
                        for j in range(len(header[key])):
                            txt = self.cols[k][key][j]
                            self.cols[k][key][j] = txt.replace(self._previous, value)
            self._previous = value
            return value, [], self.cols
        else:
            return self._previous, data, self.cols


