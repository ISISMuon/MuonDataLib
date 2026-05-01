from dash import html, callback, Output, Input
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
                dbc.Col(dbc.Input(id='min-time',
                                  value=0.,
                                  type='number')),
                dbc.Col(dbc.Input(id='max-time',
                                  value=32.768,
                                  type='number')),
                ]),
            dbc.Row(
                dbc.Col(["Number of bins:",
                     dbc.Input(id='num-bin',
                               value=2048,
                               type='number',
                               step=1),
                ])),
            dbc.Row([html.Div(id="display-width"),
                ]),
            ])

    def set_callbacks(self, presenter):
        """
        Set callbacks required by the GUI.
        """
        callback(Output('display-width', 'children'),
                 Input('min-time', 'value'),
                 Input('max-time', 'value'),
                 Input('num-bin', 'value'))(presenter.display_width)



