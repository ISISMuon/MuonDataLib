from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.histogram_settings.view import HistSettingsView


class HistSettingsPresenter(PresenterTemplate):
    """
    A class for the presenter of the histogram settings widget.
    """

    def __init__(self): 
        self._view = HistSettingsView(self)

    def display_width(self, min_time, max_time, num_bin):
        """
        Calculate bin width of a histogram from a range and number of bins.
        :param min_time: The lower limit of the range.
        :param max_time: The upper limit of the range.
        :param num_bin: The number of bins.
        :returns: The width of each bin.
        """
        return "Resolution: {:.5f}".format(abs(max_time - min_time) / num_bin)
