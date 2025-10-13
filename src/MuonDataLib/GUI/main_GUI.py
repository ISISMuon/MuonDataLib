from MuonDataLib.GUI.utils.main_window import MainDashWindow
from MuonDataLib.GUI.main_app import main_app
from dash import Input, Output, callback

import sys
from PyQt5 import QtWidgets


def launch_GUI():
    """
    A simple method to launch the help pages.
    """
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainDashWindow(main_app())

    # these should all be in the main window not here!!!!!!!

    # open file browser on load
    callback(
             Output('name', 'children'),
             Input('Load', 'n_clicks'),
             prevent_initial_call=True)(mainWin.open)

    callback(
             Output('title_test', 'children'),
             Input('load_filters', 'n_clicks'),
             prevent_initial_call=True)(mainWin.open_json)

    # open file browser on save (nxs)
    callback(
             Output('name2', 'children'),
             [Input('Save', 'n_clicks'),
              Input('save_filters', 'n_clicks')],
             prevent_initial_call=True)(mainWin.save)

    mainWin.show()
    sys.exit(app.exec_())
