from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.plot_area.view import PlotAreaView
import plotly
from plotly.subplots import make_subplots
import numpy as np


class PlotAreaPresenter(PresenterTemplate):
    def __init__(self):
        self._view = PlotAreaView(self)

    def plot(self, x1, y1, x2, y2):
        self.n_rows = 2
        self.n_cols = 1

        x = [x1, x2]
        y = [y1, y2]
        
        y_labels = ["Field (filtered)", "Temp (unfiltered)"]
        fig = make_subplots(rows=self.n_rows, cols=self.n_cols,
                            x_title='time',
                                  shared_xaxes=True,
                                  vertical_spacing=0.02,
                                  start_cell='top-left')
        # this makes sure that the legend selection is preserved unless the
        # selected plots change
        self._height = 900
        #self._keep_state = True
        fig.update_layout(height=self._height)#, uirevision=self._keep_state)

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                #inadex = 0 # self.get_index(detectors, i, j)
                fig.add_trace(plotly.graph_objects.Scatter(
                        x=x[i],
                        y=y[i], #[str(spec)],
                        name=f'Example plot: {y_labels[i]}',
                        mode='lines',
                        )
                        , i + 1, j + 1)
                fig.update_yaxes(title_text=y_labels[i], row=i+1, col=j+1)
        return fig

    #def plot(self, n_clicks):
    #    x = np.linspace(0, n_clicks)
    #    y = np.array([np.sin(x), 2*x])
    #    self.n_rows = 2
    #    self.n_cols = 1

    #    y_labels = ["Field", "Temp"]
    #    fig = make_subplots(rows=self.n_rows, cols=self.n_cols,
    #                        x_title='time',
    #                              shared_xaxes=True,
    #                              vertical_spacing=0.02,
    #                              start_cell='top-left')
    #    # this makes sure that the legend selection is preserved unless the
    #    # selected plots change
    #    self._height = 900
    #    #self._keep_state = True
    #    fig.update_layout(height=self._height)#, uirevision=self._keep_state)

    #    for i in range(self.n_rows):
    #        for j in range(self.n_cols):
    #            #inadex = 0 # self.get_index(detectors, i, j)
    #            fig.add_trace(plotly.graph_objects.Scatter(
    #                    x=x,
    #                    y=y[i], #[str(spec)],
    #                    name=f'Example plot: {y_labels[i]}',
    #                    mode='lines+markers',
    #                    )
    #                    , i + 1, j + 1)
    #            fig.update_yaxes(title_text=y_labels[i], row=i+1, col=j+1)
    #    return fig
