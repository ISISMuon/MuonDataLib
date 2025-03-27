from MuonDataLib.GUI.worker import Worker

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QVBoxLayout


class MainDashWindow(QtWidgets.QMainWindow):
    """
    A main window for the stand alone GUI
    that contains the dash app.
    """
    def __init__(self, dash_app, parent=None):
        """
        Creates the main window for the dash app.
        :param dash_app: the dash app we want to embed,
        it should not be running
        :param parent: the parent of the GUI (typically
        None)
        """
        super().__init__(parent)
        self.mainWidget = MainWidget(dash_app)
        self.setCentralWidget(self.mainWidget)

    def closeEvent(self, event):
        """
        When the GUI is closed, this makes
        sure that the Dash app and thread
        is terminated gracefully
        """
        super(MainDashWindow, self).closeEvent(event)
        self.mainWidget.worker.terminate()


class MainWidget(QWidget):
    """
    This creates the main widget for the
    GUI. It is a light weight wrapper
    around dash. The expectation is that
    the GUI will be a Dash app.
    """
    def __init__(self, dash_app, parent=None):
        super().__init__(parent)
        self.threadpool = QThreadPool()
        self.worker = Worker(dash_app)
        self.threadpool.start(self.worker)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.worker.get_address))
        lay = QVBoxLayout(self)
        lay.addWidget(self.browser)
