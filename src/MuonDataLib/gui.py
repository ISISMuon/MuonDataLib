import sys

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (QRunnable, Slot, QThreadPool)
import dash
import dash_core_components as dcc
import dash_html_components as html
from PySide6.QtWidgets import (QLineEdit, QPushButton,
                               QVBoxLayout)
import signal
import os


def run_dash(data, layout):
    app = dash.Dash()

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        ])
    app.run(debug=False)


class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @Slot()  # QtCore.Slot
    def run(self):
        data = [

            {'x': [1, 2, 3], 'y': [4, 1, 2],
             'type': 'bar', 'name': 'SF'},
            {'x': [1, 2, 3], 'y': [2, 4, 5],
             'type': 'bar', 'name': u'Montréal'},
        ]
        layout = {
           'title': 'Dash Data Visualization'
        }
        app = dash.Dash()
        app.layout = html.Div(children=[
            html.H1(children='Hello Dash'),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': data,
                    'layout': layout
                })
            ])
        app.run(debug=False, port=8015, host='127.0.0.1')

    @staticmethod
    def terminate():
        os.kill(os.getpid(), signal.SIGTERM)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)

    def closeEvent(self, event):
        super(MainWindow, self).closeEvent(event)
        self.mainWidget.worker.terminate()


class MainWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.threadpool = QThreadPool()
        # Any other args, kwargs are passed to the run function
        self.worker = Worker()
        self.threadpool.start(self.worker)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8015/"))
        self.btn = QPushButton('Button', self)
        self.btn.resize(self.btn.sizeHint())
        self.edit = QLineEdit("Write my name here")

        lay = QVBoxLayout(self)
        lay.addWidget(self.btn)
        lay.addWidget(self.browser)
        lay.addWidget(self.edit)

        self.btn.clicked.connect(self.greetings)

    def greetings(self):
        print("Hello %s" % self.edit.text())
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
