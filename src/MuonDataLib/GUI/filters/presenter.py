from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.filters.view import FilterView


class FilterPresenter(PresenterTemplate):
    def __init__(self):
        self._view = FilterView(self)
