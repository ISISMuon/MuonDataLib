from MuonDataLib.GUI.view_template import ViewTemplate

from dash import Input, Output, State, callback, html
import dash_bootstrap_components as dbc


class ControlPaneView(ViewTemplate):
    """
    Creates the main dash app for event filtering.
    """

    def generate(self, presenter):
        """
        Create the view for the app
        :param presenter: the presenter for the widget
        :returns: the app's view
        """

        # set width of the filter tables
        filter_width = 2

        # setup the layout
        return dbc.Row([
                    dbc.Col(presenter._filter.layout, width=filter_width),
                    dbc.Col(presenter._plot.layout, width=12-filter_width)
                    ],
                        className="g-0", align='center')

    def set_callbacks(self, presenter):
        """
        Set the callbacks for the widget
        :param pressenter: the presenter for the widget
        """
        callback(Output('example_plot', 'figure', allow_duplicate=True),
                 Input('time-table', 'data'),
                 [State('dropdown-time', 'value')],
                 prevent_initial_call=True)(presenter.add_filter)

        callback([Output('tooltip', 'show', allow_duplicate=True),
                  Output('tooltip', 'bbox', allow_duplicate=True),
                  Output('tooltip', 'children', allow_duplicate=True)],
                 Input('example_plot', 'hoverData'),
                 [State('time-table', 'data'),
                  State('dropdown-time', 'value')],
                 prevent_initial_call=True)(presenter.display_hover)

    def hover_text(self, pt, txt=''):
        """
        A method to generate the text for the tooltip
        (hover text).
        :param pt: the information about the point being hovered on
        :param txt: the text string we want to add to the tooltip
        :returns: An updated layout for the tooltip
        """
        children = html.Div([
            html.H5('Data Point'),
            html.P(f"x: {pt['x']:.3f},  y: {pt['y']:.3f}"),
            html.H5('Status'),
            html.P(txt)
            ])
        return children
