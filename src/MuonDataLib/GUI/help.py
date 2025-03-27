from MuonDataLib.GUI.main_window import MainDashWindow
from MuonDataLib.help.help import help_app

import sys
from PySide6 import QtWidgets


def launch_help():
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainDashWindow(help_app())
    mainWin.show()
    sys.exit(app.exec_())
