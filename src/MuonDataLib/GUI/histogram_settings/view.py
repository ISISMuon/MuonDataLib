from dash import html, dcc
import dash_bootstrap_components as dbc

from MuonDataLib.GUI.view_template import ViewTemplate


class HistSettingsView(ViewTemplate):
    """
    A class for the view of the histogram settings widget.
    """

    def generate(self, presenter):
        """
        Generate the histogram settings widget.
        :param presenter: The presenter for the widget.
        :returns: The layout for the GUI widget.
        """
        return html.Div([
            "Minimum and maximum time:",
            dbc.Row([
                dbc.Col(dcc.Input(id='min-time', 
                                  value=0,
                                  type='numeric')),
                dbc.Col(dcc.Input(id='max-time',
                                  value=32.768,
                                  type='numeric')),
                ]),
            dbc.Row(
                dbc.Col(["Resolution:", 
                     dcc.Input(id='width',
                               value=0.016,
                               type='numeric'),
                ])),
            ])


