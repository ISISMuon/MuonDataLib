from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, State


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
        :param presenter: the presenter for the widget
        :returns: the layout of the widget's
        GUI.
        """
        return html.Div([
            html.H3("Title: testing", id='title_test'),
            dbc.Accordion([
                dbc.AccordionItem(
                    [presenter._time.layout],
                    title="Time filters"),
                ],
                         start_collapsed=True),
            html.P('', id='title_test_body'),
            dbc.Button('Calculate', id='calc_btn', color='primary', className='me-md-2'),
            html.P(self.no_events_str, id='N_events'),
            ])

    def set_callbacks(self, presenter):
        """
        Sets the callbacks for the widget
        :param presenter: the presenter for the widget
        """
        callback([Output('N_events', 'children'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('calc_btn', 'n_clicks'),
                 [State('time-table', 'data'),
                  State('dropdown-time', 'value')],
                 prevent_initial_call=True)(presenter.calculate)
 
        callback(Output('N_events', 'children', allow_duplicate=True),
                 Input('time-table_changed_state', 'data'),
                 State('N_events', 'children'),
                 prevent_initial_call=True)(presenter.update_N_events)

    @property
    def no_events_str(self):
        return NUM + NC


    def get_N(self, N):
        """
        Gets the updated GUI componenet for the 
        number of events.
        :param N: the number of events
        """
        return html.P(NUM + str(N))

