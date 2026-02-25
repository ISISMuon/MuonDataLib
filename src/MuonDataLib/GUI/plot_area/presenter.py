from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.plot_area.view import PlotAreaView
import plotly
from plotly.subplots import make_subplots
import numpy as np


class PlotAreaPresenter(PresenterTemplate):
    """
    A class for the plotting widget's presenter.
    This follows the MVP pattern.
    """

    def __init__(self, ID):
        """
        Creates a Plot Area Presenter.
        This widget deals with plotly.
        We have multiple plots, so need a
        way to tell them apart.
        :param ID: the ID (unique name) for
        the plot presenter.
        """
        self.ID = ID
        self._view = PlotAreaView(self)
        self.reset_plot_range()
        self.fig = None

    def reset_plot_range(self):
        """
        Resets the plot range.
        So when new data is plotted
        it will correctly get the
        min and max time values.
        """
        self._min = 1000
        self._max = -1000

    def add_shaded_region(self, start, stop):
        """
        Adds a shaded region to the plot.
        :param start: when to start the shaded
        region
        :param stop: when to stop the shaded region
        """
        self.fig.add_vrect(x0=start,
                           x1=stop,
                           opacity=0.3,
                           fillcolor='PaleGreen',
                           layer='above',
                           line={'color': 'black',
                                 'width': 4})

    def shade_all(self):
        """
        For a new main plot, lets assume all of
        the data is shaded (included)
        """
        self.add_shaded_region(self._min, self._max)

    def new_plot(self, names, logs):
        """
        A method to create a plot from the
        sample logs. This will always create a
        fresh plot.
        :param names: a list of sample log names
        to plot
        :param logs: the sample logs object
        :returns the figure object
        """
        N = len(names)

        if N == 0:
            return self.fig

        # only stack vertically
        self.fig = make_subplots(rows=N,
                                 cols=1,
                                 x_title='time',
                                 shared_xaxes=True,
                                 vertical_spacing=0.02,
                                 start_cell='top-left')
        self._height = 900
        self.fig.update_layout(height=self._height)

        # add data to the subplots
        for i, name in enumerate(names):
            # plot lines as this is much faster than points
            log_data = logs.get_sample_log(name)
            x, y = log_data.get_original_values()
            self.fig.add_trace(plotly.graph_objects.Scatter(
                        x=x,
                        y=y,
                        name=name,
                        mode='lines'
                        ),
                              i + 1, 1)
            if self._min > np.min(x):
                self._min = np.min(x)

            if self._max < np.max(x):
                self._max = np.max(x)
            self.fig.update_traces(hoverinfo='none')
            self.fig.update_yaxes(title_text=name, row=i+1, col=1)
        return self.fig
