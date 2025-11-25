from MuonDataLib.GUI.view_template import ViewTemplate
from dash import dcc, html
from dash import Input, Output, callback, State

class PlotAreaView(ViewTemplate):
    """
    Create the view for the Plot Area widget.
    This follows the MVP pattern.
    """
    def generate(self):
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

    def set_callbacks(self, presenter):
        callback(Output('example_plot', 'figure', allow_duplicate=True),
                 Input('time-table', 'data'),
                 State('example_plot', 'figure'),
                 prevent_initial_call=True)(presenter.add_filter)

        callback([Output('tooltip', 'show', allow_duplicate=True),
                  Output('tooltip', 'bbox', allow_duplicate=True),
                  Output('tooltip', 'children', allow_duplicate=True)],
                 Input('example_plot', 'hoverData'),
                 State('time-table', 'data'),
                 prevent_initial_call=True)(presenter.display_hover)

    def hover_text(self, pt, txt=[]):
        filters = html.Div([html.P(name) for name in txt])
        children = html.Div([
            html.H5('Data Point'),
            html.P(f"x: {pt['x']:.3f},  y: {pt['y']:.3f}"),
            html.H5('Active Filters'),
            filters
            ])
        return children
