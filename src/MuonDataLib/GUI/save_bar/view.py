from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc


class SaveBarView(ViewTemplate):

    def generate(self):
        return html.Div([
            dbc.Button('Save', id='Save', color='primary',
                       n_clicks=0, className="me-md-2"),
            dbc.Button('Save filters', id='save_filters', color='primary',
                       n_clicks=0, className='me-md-2'),

            html.Div(id='name2', children="NONE", hidden=True),
            html.Div(id='name3', children="NONE", hidden=True),
            ],
                        className="d-grid gap-2 d-md-flex "
                                  "justify-content-md-start")

    def set_callbacks(self, presenter):
        return
