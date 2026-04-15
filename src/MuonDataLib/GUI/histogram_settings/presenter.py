from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.histogram_settings.view import HistSettingsView


class HistSettingsPresenter(PresenterTemplate):
    """
    A class for the presenter of the histogram settings widget.
    """

    def __init__(self): 
        self._view = HistSettingsView(self)
