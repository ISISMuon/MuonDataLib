from MuonDataLib.GUI.load_bar.presenter import LoadBarPresenter
from MuonDataLib.GUI.load_bar.view import CURRENT
from MuonDataLib.GUI.save_bar.presenter import SaveBarPresenter
from MuonDataLib.GUI.filters.presenter import FilterPresenter
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter


from MuonDataLib.data.utils import create_data_from_function
from MuonDataLib.data.loader.load_events import load_events
import numpy as np
import dash
from dash import Dash, Input, Output, State, callback, dcc, html
import dash_bootstrap_components as dbc


def osc(x, amp, omega, phi):
    """
    This creates some data to represent
    sample logs within the GUI.

    It will be removed.

    """
    return amp*np.sin(x*omega + phi)


class main_app(Dash):
    """
    Creates the main dash app for event filtering.
    """
    def __init__(self):
        """
        Creates a Dash app that can be used. This one is for
        the main GUI.
        """
        super().__init__(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        # get presenters
        self.load = LoadBarPresenter()
        self.plot = PlotAreaPresenter()
        self.save = SaveBarPresenter()
        self.filter = FilterPresenter()

        filter_width = 2

        # setup the layout
        self.layout = dbc.Container(
            [
                html.H1(
                    "MuonDataGUI",
                    style={"textAlign": "center"},
                    className="mb-3"),

                # place the notifcations just under the title
                dbc.Alert([html.H4("ERROR MESSAGE", className='alert-heading'),
                           html.P("Error", id='error_msg')],
                          id='error',
                          dismissable=True,
                          fade=False,
                          color='danger',
                          is_open=False),
                # ------------------------------------------------- #

                # this is also placed inside Loading, so it produces
                # a nice loading message when the GUI is busy.
                dcc.Loading([self.load.layout,
                             dbc.Row([
                                 dbc.Col(self.filter.layout,
                                         width=filter_width),
                                 dbc.Col(self.plot.layout,
                                         width=12-filter_width)],
                                     className="g-0", align='center'),
                             self.save.layout,
                             ],
                            overlay_style={"visibility": "visible",
                                           "opacity": .5,
                                           "backgroundColor": "white"},
                            custom_spinner=html.H2(["Please wait ... ",
                                                    dbc.Spinner(color="danger")
                                                    ],
                                                   id='spinner')
                            ),

                ],
            fluid=True,
        )
        self.set_callbacks()

    def set_callbacks(self):
        """
        A method to setup all of the callbacks needed
        by the GUI.

        Callbacks should all have unique Output's. However,
        we want several things to be able to return an
        error message. Instead of using the callback
        context to determine what was called (and a long
        if elif block) it was decided to use the
        'allow_duplicate' option instead.
        """
        # opens the error notifcation if the error message changes
        callback(Output('error', 'is_open'),
                 Input('error_msg', 'children'),
                 prevent_initial_call=True)(self.alert)

        # Updates the information on the loaded filter. With error
        # catching.
        callback([Output('title_test_body', 'children'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('title_test', 'children'),
                 State('debug', 'on'),
                 prevent_initial_call=True)(self.load_filter)

        # Plots the data after it is loaded.
        callback([Output('example_plot', 'figure'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('file_name', 'children'),
                 State('debug', 'on'),
                 prevent_initial_call=True)(self.load_nxs)

        # Turns on debug mode
        callback(dash.dependencies.Input('debug', 'on'),
                 prevent_initial_call=True)(self.debug)

        # Saves the data (both histogram and filter file).
        callback([Output('save_exe_dummy', 'children'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('save_btn_dummy', 'children'),
                 State('debug', 'on'),
                 prevent_initial_call=True)(self.save_data)

        return

    def debug(self, state):
        """
        This prints a notifcation that the debug mode
        is on. This will not be a long term feature
        and is here for testing. Debug mode just
        casues all of the methods to throw errors.
        :param state: if debug mode is on or off (bool)
        """
        tmp = 'off'
        if state:
            tmp = 'on'

        print("debug mode " + tmp)

    def load_filter(self, name, debug):
        """
        Loads a filter file into the GUI
        and applies it to the muon
        event data.
        :param name: The name of the filter file
        :param debug: If debug mode is on or off
        :returns: A text string of the filters
        and an error message (if it fails)
        """
        text = ''
        try:
            if debug:
                raise RuntimeError("Filter error")
            text = self.load.load_filters(name[len(CURRENT):])
            return text, ''
        except Exception as err:
            return '', f'Load filter error: {err}'

    def alert(self, text):
        """
        Opens the alert if new information
        has been uploaded.
        :param text: the text to be displayed in
        the alert.
        :returns: if to open the alert
        """
        if text == '':
            return False
        return True

    def save_data(self, name, debug):
        """
        Saves either a muon histogram nexus file
        or a filter file, from the current muon
        event data.
        :param name: a string of the data type (json
        or nexus) and the name of the file to save to.
        :param debug: if debug mode is on or off.
        :returns: the name of the saved file and
        the alert message
        """
        if 'None' in name:
            return '', ''
        dtype = name[0]
        file = name[1:]
        try:
            if debug:
                raise RuntimeError("Saving error")

            print("saving to ", file)
            if dtype == "n":
                self._data.save_histograms(file)
            elif dtype == 'j':
                self._data.save_filters(file)
            return file, ''
        except Exception as err:
            return '', f'Saving Error: {err}'

    def gen_fake_data(self):
        """
        This creates fake data for the sample log.
        It will not be present long term.
        We assume one data point per second.
        """
        frame_start_times = self._data.get_frame_start_times()
        start = frame_start_times[0]
        end = frame_start_times[-1] + 1
        # 1 days worth of logs at 1 per second
        N = 60*60*24
        step = (end - start)/N
        return create_data_from_function(start, end,
                                         step,
                                         [3, 6.1, 0.91],
                                         osc, seed=1)

    def load_nxs(self, name, debug_state):
        """
        Loads a muon event nexus file.
        :param name: the 'CURRENT' text string and
        the name of the file to open.
        :param debug_state: if debug mode is on or off.
        :returns: the updated figure and the alert message
        """
        if 'None' in name:
            return self.plot.plot([], [], [], []), ''
        try:
            if debug_state:
                raise RuntimeError("Loading error")

            # assume HIFI data for now, hence the magic 64 detectors.
            self._data = load_events(name[len(CURRENT):], 64)
            self.load._data = self._data

        except Exception as err:
            self._data = None
            return self.plot.plot([], [], [], []), f'An error occurred {err}'

        # add fake sample log data
        x, y = self.gen_fake_data()
        self._data.add_sample_log("Test", x, y)

        # add a filter to test the save method
        self._data.keep_data_sample_log_above("Test", -0.2)

        # this will be user defined later. For now lets just
        # load the big data set we have made
        log = self._data._get_sample_log("Test")
        a, b = log.get_values()

        return self.plot.plot(a, b, x, y), ''
