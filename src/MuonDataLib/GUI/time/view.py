from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import Input, Output, callback, State
from collections import Counter


class DefaultValues(object):
    def __init__(self):
        self.count = 0

    def generate(self):
        self.count += 1
        return {'Name_t': f'default_{self.count}',
                'Type_t': 'Exclude', 
                'Start_t': 500, 
                'End_t': 1000}

def moo(text):
    print(text)
    return '#0074D9'

class TimeView(ViewTemplate):
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
        self.default = DefaultValues()
        self._page = self.generate()
        self.set_callbacks()

    def generate(self):
        """
        Creates the filter widget's GUI.
        :returns: the layout of the widget's
        GUI.
        """
        return html.Div([
            dbc.Button(id='time_add_row', class_name='bi-plus-lg'),
            html.H3(""),
            dash_table.DataTable(
        id='time-table',
        data=[],
        columns=[
            {'id': 'Name_t', 'name': 'Name'},
            {'id': 'Type_t', 'name': 'Data', 'presentation': 'dropdown'},
            {'id': 'Start_t', 'name': 'Start', 'type':'numeric'},
            {'id': 'End_t', 'name': 'End', 'type':'numeric'},
        ],
        css=[{"selector": ".Select-menu-outer", "rule": "display : block!important"}],
        editable=True,
        style_cell={"textAlign": "center"},
        dropdown={
            'Type_t': {
                'clearable':False,
                'options': [
                    {'label': "Include", 'value': "Include"},
                    {'label': "Exclude", 'value': "Exclude"},
                ],
            },
        },
 
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Type_t} contains "Include"',
                    'column_id': ['Name_t', 'Start_t', 'End_t'],
                    },
                'backgroundColor': 'PowderBlue',#'#0074D9',
                'color': 'white',
                },
            {
                'if': {
                    'filter_query': '{Type_t} contains "Exclude"',
                    'column_id': ['Name_t', 'Start_t', 'End_t'],
                    },
                'backgroundColor': 'orangered',#'#85144b',
                'color': 'white',
                },


 
            ],
       row_deletable=True,
    ),
    html.Div(id='table-dropdown-container')
 
                    ])

    def set_callbacks(self):
        callback(Output('time-table', 'data', allow_duplicate=True),
                 Input('time_add_row', 'n_clicks'),
                 State('time-table', 'data'),
                 prevent_initial_call=True,
                 allow_duplicate=True)(self.add)
 
        callback([Output('time-table', 'data', allow_duplicate=True),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('time-table', 'data_timestamp'),
                 [State('time-table', 'data'),
                  State('time-table', 'data_previous')],
                 prevent_initial_call=True)(self.update)
 
    def validate_cols(self, new_row, old_row):
        if new_row['Start_t'] > new_row['End_t']:
            return False, f'Start time {new_row["Start_t"]} is greater than end time {new_row["End_t"]}'
        return True, ''

    def validate(self, data, previous):
        if len(data) == 0:
            return True, ''

        names = [row['Name_t'] for row in data]
        repeat, num = Counter(names).most_common(1)[0]
        if num > 1:
            return False, f'Repeated name {repeat}'

        for new_row, old_row in zip(data, previous):
            if new_row != old_row:
                return self.validate_cols(new_row, old_row)
        return True, ''

    def update(self, timestamp, data, previous):
        """
        This allows the user to change a value and then
        click out of the cell (without pressing enter)
        such that the table keeps the new value
        """
        valid, msg = self.validate(data, previous)
        if valid:
            return data, ''
        return previous, msg

    def add(self, n, data):
        data.append(self.default.generate())
        return data
