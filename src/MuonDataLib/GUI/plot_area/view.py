from MuonDataLib.GUI.view_template import ViewTemplate
from dash import dcc, html
from dash import Input, Output, callback, State

class PlotAreaView(ViewTemplate):
    """
    Create the view for the Plot Area widget.
    This follows the MVP pattern.
    """
    def generate(self, presenter):
        """
        Creates the layout for the widget.
        :returns: the layout for the view.
        """
        return html.Div([
            html.Div(dcc.Graph(id='example_plot',
                               clear_on_unhover=True),
                     style={'width': '100%',
                            'display': 'inline-block',
                            'padding': '0 20'}),
            dcc.Tooltip(id='tooltip'),
                     ])

