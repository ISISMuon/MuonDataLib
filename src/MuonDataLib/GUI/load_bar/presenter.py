from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.load_bar.view import LoadBarView
from MuonDataLib.data.loader.load_events import load_events


class LoadBarPresenter(PresenterTemplate):
    def __init__(self):
        self._view = LoadBarView(self)
        self._data = None
        self._load_btn_press = 0
        self._load_filter_press = 0

    def load_btn_pressed(self, n_clicks):
        if n_clicks > self._load_btn_press:
            self._load_btn_press += 1
            return True
        return False

    def load_filter_pressed(self, n_clicks):
        if n_clicks > self._load_filter_press:
            self._load_filter_press += 1
            return True
        return False


    def load_nxs(self, name):
        self._data = load_events(name, 64)

    @property
    def get_data(self):
        return self._data
