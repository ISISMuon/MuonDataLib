from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.save_bar.view import SaveBarView


class SaveBarPresenter(PresenterTemplate):
    def __init__(self):
        self._view = SaveBarView(self)
        self._save_btn_press = 0
        self._save_filter_press = 0

    def save_btn_pressed(self, n_clicks):
        if n_clicks > self._save_btn_press:
            self._save_btn_press += 1
            return True
        return False

    def save_filter_pressed(self, n_clicks):
        if n_clicks > self._save_filter_press:
            self._save_filter_press += 1
            return True
        return False


