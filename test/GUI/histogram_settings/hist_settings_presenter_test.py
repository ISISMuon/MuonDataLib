"""Tests for the histogram settings presenter."""
from MuonDataLib.GUI.histogram_settings.presenter import HistSettingsPresenter
from MuonDataLib.test_helpers.unit_test import TestHelper

class HistogramSettingsPresenterTest(TestHelper):

    def setUp(self):
        self.presenter = HistSettingsPresenter()

    def test_display_width(self):
        """
        Test that the resolution is correctly displayed
        for valid settings.
        """
        output = self.presenter.display_width(0, 10, 2)
        assert output == "Resolution: 5.00000"

        output = self.presenter.display_width(0, 1, 3)
        assert output == "Resolution: 0.33333"

    def test_display_width_invalid(self):
        """
        Test that no resolution is displayed if num_bins
        is zero or not entered.
        """
        for num_bins in [0, None]:
            output = self.presenter.display_width(0, 4, num_bins)
            assert output == "Resolution: "
