from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import Input, Output, callback, State
from collections import Counter


class TableView(ViewTemplate):
    """
    A class for the view of the filter
    table. This follows the MVP
    pattern.
    """

    def generate(self, presenter):
        """
        Creates the filter widget's GUI.
        :returns: the layout of the widget's
        GUI.
        """

        return html.Div([
            dbc.Button(id=presenter.ID+ '_add', class_name='bi-plus-lg'),
            html.H3(""),
            dash_table.DataTable(
        id=presenter.ID,
        data=[],
        columns=presenter.cols,
        css=[{"selector": ".Select-menu-outer", "rule": "display : block!important"}],
        editable=True,
        style_cell={"textAlign": "center"},
        style_table={'overflowX': 'auto'},
        dropdown=presenter.options,
        style_data_conditional=presenter.conditions,
        merge_duplicate_headers=True,
        row_deletable=True,
    ),
    html.Div(id='table-dropdown-container')
                    ])

    def set_callbacks(self, presenter):
        callback(Output(presenter.ID, 'data', allow_duplicate=True),
                 Input(presenter.ID + '_add', 'n_clicks'),
                 State(presenter.ID, 'data'),
                 prevent_initial_call=True,
                 allow_duplicate=True)(presenter.add)
 
        callback([Output(presenter.ID, 'data', allow_duplicate=True),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input(presenter.ID, 'data_timestamp'),
                 [State(presenter.ID, 'data'),
                  State(presenter.ID, 'data_previous')],
                 prevent_initial_call=True)(presenter.update)
