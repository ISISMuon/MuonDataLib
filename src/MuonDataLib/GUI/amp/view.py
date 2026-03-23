from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html, dcc
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc


class AmplitudeView(ViewTemplate):
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
            presenter._plot.layout,
            html.Div(['Amplitude threshold', dcc.Input(id='Amp', value=0, type='numeric')])
            ])

    def set_callbacks(self, presenter):
        """
        Sets the callbacks for the GUI.
        Have additional callbacks for:
        - updating the data in the pop up
        - closing the pop up
        - setting the combo box options and value when
        opening the pop up
        :param presenter: the presenter object
        """
        super().set_callbacks(presenter)

        #callback([Output('log_plot', 'figure', allow_duplicate=True),
        #          Output('log_max', 'children'),
        #          Output('log_mean', 'children'),
        #          Output('log_min', 'children'),
        #          Output('log_std', 'children'),],
        #         Input('log_selection', 'value'),
        #         prevent_initial_call=True)(presenter.show_log_data)

