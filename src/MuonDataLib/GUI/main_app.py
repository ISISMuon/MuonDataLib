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
    return amp*np.sin(x*omega + phi)


class main_app(Dash):
    def __init__(self):
        """
        Creates a Dash app that can be used. This one is for
        the main GUI.
        """
        super().__init__(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        self.load = LoadBarPresenter()
        self.plot = PlotAreaPresenter()
        self.save = SaveBarPresenter()
        self.filter = FilterPresenter()

        filter_width = 2

        self.layout = dbc.Container(
            [
                html.H4(
                    "MuonDataGUI",
                    style={"textAlign": "center"},
                    className="mb-3"),
                dbc.Alert([html.H4("ERROR MESSAGE", className='alert-heading'),
                           html.P("Error", id='error_msg')],
                          id='error',
                          dismissable=True,
                          fade=False,
                          color='danger',
                          is_open=False),
                # ------------------------------------------------- #
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
                                                     dbc.Spinner(color="danger"
                                                                 )],
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
        """
        callback(Output('error', 'is_open'),
                 Input('error_msg', 'children'),
                 prevent_initial_call=True)(self.warning)

        callback([Output('title_test_body', 'children'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('title_test', 'children'),
                 State('debug', 'on'),
                 prevent_initial_call=True)(self.load_filter)


        callback([Output('example_plot', 'figure'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('file_name', 'children'),
                 State('debug', 'on'),
                 prevent_initial_call=True)(self.load_nxs)

        callback(dash.dependencies.Input('debug', 'on'),
                 prevent_initial_call=True)(self.debug)

        callback([Output('save_exe_dummy', 'children'),
                  Output('error_msg', 'children', allow_duplicate=True)],
                 Input('save_btn_dummy', 'children'),
                 State('debug', 'on'),
                 prevent_initial_call=True)(self.save_data)

        return

    def debug(self, state):
        tmp = 'off'
        if state:
            tmp = 'on'

        print("debug mode " + tmp)

    def load_filter(self, name, debug):
        text = ''
        try:
            if debug:
                raise RuntimeError("Filter error")
            text = self.load.load_filters(name[len(CURRENT):])
            return text, ''
        except Exception as err:
            return '', f'Load filter error: {err}'
        
    def warning(self, text):
        if text == '':
            return False
        return True


    def save_data(self, name, debug):
        if 'None' in name:
            return ''#, ''
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
        if 'None' in name:
            return self.plot.plot([], [], [], []), ''
        try:
            if debug_state:
                raise RuntimeError("Loading error")

            self._data = load_events(name[len(CURRENT):], 64)
            self.load._data = self._data
        except Exception as err:
            self._data = None
            return self.plot.plot([], [], [], []), f'An error occurred {err}'

        x, y = self.gen_fake_data()
        self._data.add_sample_log("Test", x, y)
        # add a filter to test the save method
        self._data.keep_data_sample_log_above("Test", -0.2)

        # this will be user defined later. For now lets just
        # load the big data set we have made
        log = self._data._get_sample_log("Test")
        a, b = log.get_values()
        return self.plot.plot(a, b, x, y), ''
