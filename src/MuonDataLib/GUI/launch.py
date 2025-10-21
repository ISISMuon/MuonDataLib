from MuonDataLib.GUI.utils.main_window import MainDashWindow
import sys
from PyQt5 import QtWidgets


def launch_dash(dash_app):
    """
    A simple method to launch a dash app
    as part of a stand alone GUI.
    This works by placing the dash app
    inside of a pyqt web browser.
    """
    app = QtWidgets.QApplication(sys.argv)

    mainWin = MainDashWindow(dash_app)
    mainWin.show()

    sys.exit(app.exec_())
