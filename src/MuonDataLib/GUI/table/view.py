from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table, dcc
import dash_ag_grid as dag

from dash import Input, Output, callback, State

import json

class TableView(ViewTemplate):
    """
    A class for the view of a
    table. This follows the MVP
    pattern.
    """

    def generate(self, presenter):
        """
        Creates the table widget's GUI.
        :param presenter: the presenter for the GUI
        :returns: the layout of the widget's
        GUI.
        """
        self.data = [{'Delete_t': '', 'Name_t': 'moo', 'Start_t':100, 'End_t':200},
                     {'Delete_t': '', 'Name_t': 'baa', 'Start_t':1, 'End_t': 5}]

        col_defs = [

                {'field': 'Delete_t',
                 'headerName': '',
                 'width':80,
                 'editable': False,
                 "cellRenderer": "DBC_Button",
                 "cellRendererParams": {"className": "btn btn-success",
                                        'color': 'danger',
                                        'Icon': 'bi bi-trash me-2',
                                        }},
                {'field': 'Name_t', 'headerName': 'Name', 'width':100,
                                    'cellEditor': 'agLargeTextCellEditor',
                                    'cellEditorPopup': False,
                                    'cellEditorParams': {
                                                         'maxLength': 50,
                                                        }},
            {"headerName": "Include Filter details",
             'openByDefault': True,
             "children": [
                 {'field': 'Start_t', 'headerName': 'Start', 'width':100,
                  'cellEditor': 'agNumberCellEditor',
                  'cellEditorParams': {
                  'min': 0,
                  'max': 10000,
                  'precision': 3,
                }},
                 {'field': 'End_t', 'columnGroupShow': 'open', 'headerName': 'End',  'width':100,
                  'cellEditor': 'agNumberCellEditor',
                  'cellEditorParams': {
                  'min': 0,
                  'max': 10000,
                  'precision': 3,}
                  },
                 ]},
             ]

        return html.Div([
            dbc.Button(id=presenter.ID + '_add', class_name='bi-plus-lg'),
            html.H3(id='moo', children=""),
            dcc.Store(data=False, id=presenter.ID + '_changed_state'),
            dag.AgGrid(id=presenter.ID,
                       columnDefs=col_defs,
                       rowData=self.data,
                       defaultColDef={'editable': True}),
            html.H3('hi', id="test_test"),
            html.Div(id='table-dropdown-container')
            ])

    def showChange(self, n):
        return json.dumps(n)

    def test_add(self, n):
        # cant get previous values, so need to store it manually... grrr
        self.data.append({'Delete_t': '',
                          'Name_t': 'baaa',
                          'Start_t': 22,
                          'End_t': 55})
        return self.data

    def test_validate(self, change, data):
        changed = change[0]
        col_name = changed['colId']
        row = changed['data']
        new_value = row[col_name]
        if col_name == 'Start_t':
            end_value = row['End_t']
            if new_value > end_value:
                # keep the old one
                new_value = changed['oldValue']
        elif col_name == 'End_t':
            start_value = row['Start_t']
            if new_value < start_value:
                # keep the old one
                new_value = changed['oldValue']

        data[changed['rowIndex']][col_name] = new_value
        return data

    def test(self, data):
        print(data)
        return 'wsss'

    def set_callbacks(self, presenter):
        """
        Set the callbacks for the GUI.
        :param presenter: the presenter for the GUI
        """
        callback(Output(presenter.ID, 'rowData'),
                 Input(presenter.ID + '_add', 'n_clicks'),
                 prevent_initial_call=True)(self.test_add)

        callback(Output(presenter.ID, 'rowData', allow_duplicate=True),
                 Input(presenter.ID, 'cellValueChanged'),
                 State(presenter.ID, 'virtualRowData'),
                 prevent_initial_call=True)(self.test_validate)

        callback(Output("test_test", "children"),
                 Input(presenter.ID, "cellRendererData"),
                 prevent_initial_call=True)(self.test)

        """
        callback([Output(presenter.ID, 'data', allow_duplicate=True),
                  Output(presenter.ID + '_changed_state',
                         'data',
                         allow_duplicate=True)],
                 Input(presenter.ID + '_add', 'n_clicks'),
                 State(presenter.ID, 'data'),
                 prevent_initial_call=True,
                 allow_duplicate=True)(presenter.add)

        callback([Output(presenter.ID, 'data', allow_duplicate=True),
                  Output(presenter.ID + '_changed_state',
                         'data',
                         allow_duplicate=True),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input(presenter.ID, 'data_timestamp'),
                 [State(presenter.ID, 'data'),
                  State(presenter.ID, 'data_previous')],
                 prevent_initial_call=True)(presenter.update)
        """
