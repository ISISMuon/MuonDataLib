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

    def __init__(self, presenter):
        self.t = TimeView()
        super().__init__(presenter)

    def generate(self):
        """
        Creates the filter widget's GUI.
        :returns: the layout of the widget's
        GUI.
        """
        return html.Div([
            html.H3("Title: testing", id='title_test'),
            self.t._page,
            html.P('', id='title_test_body'),
            dbc.Button('Calculate', id='calc_btn', color='primary', className='me-md-2'),
            html.P(NUM + NC, id='N_events'),
            ])

    def set_callbacks(self, presenter):
        callback(Output('N_events', 'children'),
                 Input('calc_btn', 'n_clicks'),
                 prevent_initial_call=True)(presenter.calculate)

    def get_N(self, N):
        return html.P(NUM + str(N))

