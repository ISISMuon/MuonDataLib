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
        self.assertEqual(output, "Resolution: 5.00000 μs")

        output = self.presenter.display_width(0, 1, 3)
        self.assertEqual(output, "Resolution: 0.33333 μs")

    def test_display_width_invalid(self):
        """
        Test that no resolution is displayed if num_bins
        is zero or not entered.
        """
        for num_bins in [0, None]:
            output = self.presenter.display_width(0, 4, num_bins)
            self.assertEqual(output,
                             "Resolution: N/A (invalid number of bins)")
