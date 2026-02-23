from MuonDataLib.GUI.table.view import TableView
from dash import html, dcc
from dash import Input, Output, callback
import dash_bootstrap_components as dbc


class LogView(TableView):
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

        text = html.Div([html.H4('Sample log:'),
                         dcc.Dropdown(['Temp', 'B', 'Current', 'flux'],
                                      'Temp',
                                      id='log_selection',
                                      clearable=False),
                         html.Hr(),
                         html.H4('Statistics'),
                         html.P('max: 0.0'),
                         html.P('mean: 0.0'),
                         html.P('min: 0.0'),
                         html.Hr(),
                         html.P('sigme: 0.0'),
                         ])
        # set width of the text area
        filter_width = 4

        # setup the layout
        tmp = dbc.Row([
                        dbc.Col(text, width=filter_width),
                        dbc.Col(presenter._plot.layout, width=12-filter_width)
                       ],
                       className="g-0", align='center')

        btns = html.Div([dbc.Button('ok',
                                    color='secondary',
                                    id='log_ok',
                                    className='ms-auto'),
                         dbc.Button('cancel',
                                    color='secondary',
                                    id='log_cancel',
                                    className='ms-md-2')])

        return html.Div([
            dbc.Modal(
                [dbc.ModalHeader(dbc.ModalTitle('Sample log selection'),
                                 close_button=False),
                 dbc.ModalBody(tmp),
                 dbc.ModalFooter(btns)],
                id='log_selector',
                size='xl',
                is_open=False),
            super().generate(presenter)])

    def set_callbacks(self, presenter):
        super().set_callbacks(presenter)

        callback(Output('log_selector', 'is_open'),
                 [Input('log_cancel', 'n_clicks'),
                  Input('log_ok', 'n_clicks')],
                 prevent_initial_call=True)(presenter.close_modal)
