from MuonDataLib.GUI.view_template import ViewTemplate
from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px


class PlotAreaView(ViewTemplate):

    def generate(self):
        return html.Div([
                        html.Div([
                        dcc.Graph(
                            id='example_plot',
                        )
                    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),       
                        ])

    def set_callbacks(self, presenter):
        return
        #callback(Output('example_plot', 'figure'),
        #         Input('Load', 'n_clicks'),
        #         prevent_initial_call=True)(presenter.plot)


