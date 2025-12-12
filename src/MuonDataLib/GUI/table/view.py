from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import dash_ag_grid as dag
from dash import Input, Output, callback, State


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
        return html.Div([
            dbc.Button(id=presenter.ID + '_add', class_name='bi-plus-lg'),
            html.H3(id='moo', children=""),
            dcc.Store(data=False, id=presenter.ID + '_changed_state'),
            dag.AgGrid(id=presenter.ID,
                       columnDefs=presenter.cols,
                       rowData=[],
                       defaultColDef={'editable': True,
                                      'suppressMovable': True}),
            html.H3('hi', id="test_test"),
            html.Div(id='table-dropdown-container')
            ])

    def set_callbacks(self, presenter):
        """
        Set the callbacks for the GUI.
        :param presenter: the presenter for the GUI
        """
        callback(Output(presenter.ID, 'rowData'),
                 Input(presenter.ID + '_add', 'n_clicks'),
                 State(presenter.ID, 'virtualRowData'),
                 prevent_initial_call=True)(presenter.add)

        callback([Output(presenter.ID, 'rowData', allow_duplicate=True),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input(presenter.ID, 'cellValueChanged'),
                 State(presenter.ID, 'virtualRowData'),
                 prevent_initial_call=True)(presenter.validate)

        callback(Output(presenter.ID, "rowData", allow_duplicate=True),
                 Input(presenter.ID, "cellRendererData"),
                 State(presenter.ID, 'virtualRowData'),
                 prevent_initial_call=True)(presenter.delete_row)
