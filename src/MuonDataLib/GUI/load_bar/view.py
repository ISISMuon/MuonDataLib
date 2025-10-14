from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Input, Output, callback
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
            dbc.Button('Settings', id='settings', color='primary',
                       n_clicks=0, className='me-md-2'),
            dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Settings")),
                dbc.ModalFooter(
                    dbc.Row([
                    daq.BooleanSwitch(on=False, id='debug', label='Debug'),
                    ])
                ),
            ],
            id="settings_pop_up",
            is_open=False,
        )
            ],
                        className="d-grid gap-2 d-md-flex "
                                  "justify-content-md-start")

    def set_callbacks(self, presenter):
        """
        Callbacks are in main_GUI.py so they can connect to the qt
        file finder
        """
        callback(
             Output('settings_pop_up', 'is_open'),
             Input('settings', 'n_clicks'),
             prevent_initial_call=True)(self.m)


        return

    def m(self, state):
        #self.debug = state
        return True
