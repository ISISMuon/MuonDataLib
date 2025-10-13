from MuonDataLib.GUI.view_template import ViewTemplate


class PresenterTemplate(object):
    def __init__(self):
        self._view = ViewTemplate(self)

    @property
    def layout(self):
        return self._view.layout
