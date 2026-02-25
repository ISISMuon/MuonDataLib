import unittest
from MuonDataLib.GUI.plot_area.presenter import PlotAreaPresenter
from MuonDataLib.test_helpers.unit_test import TestHelper


class PlotAreaPresenterTest(TestHelper):

    def setUp(self):
        self.presenter = PlotAreaPresenter('plot_test')
        # just add a plot with 2 subplots
        self.presenter.plot(['test', 'data'],
                             [[0, 2],
                              [0, 2]],
                             [[4, 5],
                              [2, 4]])
        # clear the shapes
        self.presenter.fig.layout.shapes = []

    @property
    def get_fig(self):
        return self.presenter.fig

    def test_add_shaded_region(self):
        self.check_shapes([])

        self.presenter.add_shaded_region(0.5, 0.8)
        self.check_shapes([[0.5, 0.8, 0, 1],
                           ])

    def test_reset_plot_range(self):
        self.assertEqual(self.presenter._min,
                         0.0)
        self.assertEqual(self.presenter._max,
                         2)

        self.presenter.reset_plot_range()
        self.assertEqual(self.presenter._min,
                         1000)
        self.assertEqual(self.presenter._max,
                         -1000)


if __name__ == '__main__':
    unittest.main()
