from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc

# from MuonDataLib.GUI.utils.my_btn import my_btn

CURRENT = "Current File: "


class LoadBarView(ViewTemplate):

    def generate(self):
        return html.Div([
            dbc.Button('Load', id='Load',
                   color='primary', className='me-md-2'),
            dbc.Button('Load filters', id='load_filters', color='primary',
                       n_clicks=0, className='me-md-2'),
            html.Div(id='file_name', children=CURRENT),
            ],
                        className="d-grid gap-2 d-md-flex "
                                  "justify-content-md-start")

    def set_callbacks(self, presenter):
        """
        Callbacks are in main_GUI.py so they can connect to the qt
        file finder
        """

        return
