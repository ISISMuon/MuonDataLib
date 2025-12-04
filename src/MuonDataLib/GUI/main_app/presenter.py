from MuonDataLib.GUI.load_bar.view import CURRENT
from MuonDataLib.GUI.load_bar.presenter import LoadBarPresenter
from MuonDataLib.GUI.control_pane.presenter import ControlPanePresenter
from MuonDataLib.GUI.save_bar.presenter import SaveBarPresenter

from MuonDataLib.data.utils import create_data_from_function
import numpy as np


def osc(x, A, omega, phi):
    return A*np.sin(omega*x + phi)


class MainAppPresenter(object):

    def __init__(self, open_nxs_func):
        """
        This is the presenter for the
        main app. It follows the MVP
        pattern, but the view
        is the main app.
        :param open_nxs_func: gets the html funtion
        )
        """
        self.load = LoadBarPresenter()
        self.control = ControlPanePresenter()
        self.save = SaveBarPresenter()
        self._open_nxs_func = open_nxs_func
        self.N_submit = 0

    def open_nxs(self, n_clicks, name):
        """
        A method to open a nexus file.
        If the filters are empty it
        wwskips the confirm dialog.
        :param n_clicks: number of times submit
        has been pressed
        """
        if n_clicks > self.N_submit:
            self.N_submit += 1
            return self._open_nxs_func(self.N_submit)
        return name

    def confirm_load(self, n_clicks, data, submit):
        """
        Gives a confirm pop up iff filters are presnt.
        :param n_clicks: Number of clicks of load
        :param data: the time filter table data
        :param submit: the number of clicks of submit
        :reuturn: if to show the GUI and the state of
        the tine filters
        """
        if len(data) > 0:
            return True, submit
        return False, submit + 1

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
        :returns: A text string of the filters,
        the list of rows for the time filter table,
        the state of the time filters (include/exclude)
        and an error message (if it fails)
        """
        text = ''
        try:
            if debug:
                raise RuntimeError("Filter error")

            filters = name[len(CURRENT):]
            data, state = self.control.read_filter(filters)
            return text, data, state, ''
        except Exception as err:
            return '', [], 'Exclude', f'Load filter error: {err}'

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

    def save_data(self, name, filters, time_mode, debug):
        """
        Saves either a muon histogram nexus file
        or a filter file, from the current muon
        event data.
        :param name: a string of the data type (json
        or nexus) and the name of the file to save to.
        :param filters: the filters (list of dicts) to use
        :param time_mode: If the time filters are to include
        or exclude the data
        :param debug: if debug mode is on or off.
        :returns: the name of the saved file and
        the alert message
        """
        data = self.load.get_data
        if 'None' in name:
            return '', ''
        dtype = name[0]
        file = name[1:]
        try:
            if debug:
                raise RuntimeError("Saving error")

            print("saving to ", file, dtype)
            self.control._filter.apply_filters(filters, time_mode)
            if dtype == "n":
                data.save_histograms(file)
            elif dtype == 'j':
                data.save_filters(file)
            return file, ''
        except Exception as err:
            return '', f'Saving Error: {err}'

    def gen_fake_data(self, data):
        """
        This creates fake data for the sample log.
        It will not be present long term.
        We assume one data point per second.
        :param data: the muon event data object
        :returns: the fake data
        """
        frame_start_times = data.get_frame_start_times()
        start = frame_start_times[0]
        end = frame_start_times[-1] + 1
        # 1 days worth of logs at 1 per second
        N = 60*60*24
        step = (end - start)/N
        return create_data_from_function(start, end,
                                         step,
                                         [3, 6.1, 0.91],
                                         osc, seed=1)

    def plot(self, x0, y0, x1, y1):
        """
        A method to plot the sample log data.
        This exists to make some code cleaner
        :param x0: the first set of x values
        :param y0: the first set of y values
        :param x1: the second set of x values
        :param y1: the second set of y values
        """
        return self.control._plot.plot(x0, y0, x1, y1)

    def load_nxs(self, name, data, debug_state):
        """
        Loads a muon event nexus file.
        :param name: the 'CURRENT' text string and
        the name of the file to open.
        :param data: the time filter table data
        :param debug_state: if debug mode is on or off.
        :returns: the updated figure, the time filter table
        data and the alert message
        """
        if name == self.load.file:
            return self.control._plot.fig, data, ''
        self.load.set_file(name)

        if 'None' in name:
            return self.plot([], [], [], []), [], ''
        try:
            if debug_state:
                raise RuntimeError("Loading error")

            self.load.load_nxs(name[len(CURRENT):])

        except Exception as err:
            return self.plot([], [], [], []), [], f'An error occurred: {err}'

        data = self.load.get_data
        self.control.set_data(data)
        # add fake sample log data
        x, y = self.gen_fake_data(data)
        data.add_sample_log("Test", x, y)

        # this will be user defined later. For now lets just
        # load the big data set we have made
        log = data._get_sample_log("Test")
        a, b = log.get_values()

        return self.plot(a, b, x, y), [], ''
