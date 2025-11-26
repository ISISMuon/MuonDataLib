from MuonDataLib.GUI.view_template import ViewTemplate
from MuonDataLib.GUI.time.view import TimeView
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, callback


NUM = 'Number of events: '
NC = 'Not Calculated'


class FilterView(ViewTemplate):
    """
    A class for the view of the filter
    widget. This follows the MVP
    pattern.
    """

    def generate(self, presenter):
        """
        Creates the filter widget's GUI.
        :returns: the layout of the widget's
        GUI.
        """
        return html.Div([
            html.H3("Title: testing", id='title_test'),
            presenter._time.layout,
            html.P('', id='title_test_body'),
            html.P(NUM + NC, id='N_events'),
            ])

    def set_callbacks(self, presenter):
        callback(Output('N_events', 'children'),
                 Input('calc_btn', 'n_clicks'),
                 prevent_initial_call=True)(presenter.calculate)

    def get_N(self, N):
        return html.P(NUM + str(N))

