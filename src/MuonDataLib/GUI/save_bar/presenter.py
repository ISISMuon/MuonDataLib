from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.save_bar.view import SaveBarView


class SaveBarPresenter(PresenterTemplate):
    def __init__(self):
        self._view = SaveBarView(self)
