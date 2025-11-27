from MuonDataLib.GUI.table.presenter import TablePresenter
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

        name = Header('Name_t', 'Name')
        data = Header('Type_t', 'data')

        start = Header('Start_t', 'Start')
        start.add_type('numeric')

        end = Header('End_t', 'End')
        end.add_type('numeric')

        data.add_dropdown(['Include', 'Exclude'])
        data.add_condition('{Type_t} contains "Include"',
                           [name.ID, start.ID, end.ID],
                           'PowderBlue',
                           'Black')

        data.add_condition('{Type_t} contains "Exclude"',
                           [name.ID, start.ID, end.ID],
                           'OrangeRed',
                           'White')

        super().__init__('time-table',
                         [name, data, start, end],
                         name.ID)

    def validate_row(self, new_row, old_row):
        if new_row['Start_t'] > new_row['End_t']:
            return False, f'Start time {new_row["Start_t"]} is greater than end time {new_row["End_t"]}'
        return True, ''

    @property
    def generate_default(self):
        self.count += 1
        return {'Name_t': f'default_{self.count}',
                'Type_t': 'Exclude',
                'Start_t': 500,
                'End_t': 1000}

    def get_exc_data(self, data):
        return [data['Start_t'], data['End_t']]


