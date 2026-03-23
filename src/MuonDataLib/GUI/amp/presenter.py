from MuonDataLib.GUI.table.presenter import PresenterTemplate
from MuonDataLib.GUI.amp.view import AmplitudeView
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter
import numpy as np


class AmpPresenter(PresenterTemplate):
    """
    A class for the view of the sample log filter
    widget. This follows the MVP
    pattern.
    """
    def __init__(self):
        """
        This creates the presenter object for the
        widget.
        """

        # create a plot area
        self._plot = PlotAreaPresenter('amp')
        self._view = AmplitudeView(self)

    def plot(self, data):
        hist, bins = data.get_peak_property_histogram('Amplitudes')
        return self._plot.plot(['amplitudes'],
                               [(bins[:-1] + bins[1:])/2.],
                               [hist],
                               'Amplitude')
