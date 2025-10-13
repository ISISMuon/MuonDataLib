from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.load_bar.view import LoadBarView
from MuonDataLib.data.loader.load_events import load_events


class LoadBarPresenter(PresenterTemplate):
    def __init__(self):
        self._view = LoadBarView(self)
        self._data = None

    def load_nxs(self, name):
        self._data = load_events(name, 64)

    @property
    def get_data(self):
        return self._data
