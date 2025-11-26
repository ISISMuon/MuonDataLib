from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.plot_area.view import PlotAreaView
import plotly
from plotly.subplots import make_subplots
from dash import no_update
import numpy as np

class PlotAreaPresenter(PresenterTemplate):
    """
    A class for the plotting widget's presenter.
    This follows the MVP pattern.
    """

    def __init__(self):
        """
        Creates a Plot Area Presenter.
        """
        self._view = PlotAreaView(self)
        self._min = 1000
        self._max = -1000

    def add_filter(self, data, fig):
        #tmp = fig['layout']['xaxis']['range']
        #print('mooo', tmp, self._min)
        # clear the current filters from plot
        self.fig.layout.shapes = []
        self.fig.layout.annotations = []
        start = []
        end = []
        # add the filters back
        for filter_details in data:
            if filter_details['Type_t'] == 'Include':
                self.add_inc_data(filter_details)
            else:
                tmp = self.get_exc_data(filter_details)
                start.append(tmp[0])
                end.append(tmp[1])
                #self.add_exc_data(filter_details)
        self.apply_exc_data(start, end)

        return self.fig

    def add_inc_data(self, data):
        self.fig.add_vrect(x0=data['Start_t'], 
                           x1=data['End_t'], 
                           opacity=0.3, 
                           fillcolor='PaleGreen',
                           layer='above', 
                           line={'color':'black',
                                 'width':4}
                           )
 
    def get_exc_data(self, data):
        return [data['Start_t'], data['End_t']]

    def add_shaded_region(self, start, stop):
        self.fig.add_vrect(x0=start, 
                           x1=stop, 
                           opacity=0.3, 
                           fillcolor='PaleGreen',
                           layer='above', 
                           line={'color':'black',
                                 'width':4}
                           )
 

    def apply_exc_data(self, start, end):
        if len(start) == 0:
            return

        sorted_start = np.sort(start)
        sorted_end = np.sort(end)
        
        f_start = [sorted_start[0]]
        f_end = []
        
        for j in range(len(sorted_start)-1):
            if sorted_start[j+1] > sorted_end[j]:
                f_end.append(sorted_end[j])
                f_start.append(sorted_start[j+1])
        f_end.append(sorted_end[-1])

        self.add_shaded_region(self._min, f_start[0])
        for j in range(1, len(f_start)):
            # need to add shaded areas: these are not shaded
            print(f_start[j], f_end[j])
            self.add_shaded_region(f_end[j-1], f_start[j])
        
        self.add_shaded_region(f_end[-1], self._max)



    def add_exc_data(self, data):
        self.fig.add_vrect(x0=self._min, 
                           x1=data['Start_t'], 
                           opacity=0.3, 
                           fillcolor='PaleGreen',
                           layer='above', 
                           line={'color':'black',
                                 'width':4}
                           )
 
        self.fig.add_vrect(x0=data['End_t'], 
                           x1=self._max, 
                           opacity=0.3, 
                           fillcolor='PaleGreen',
                           layer='above', 
                           line={'color':'black',
                                 'width':4}
                           )
 

    def plot(self, x1, y1, x2, y2):
        """
        Creates a plot with 2 subplots.
        :param x1: the x values for the first subplot
        :param y1: the y values for the first subplot
        :param x2: the x values for the second subplot
        :param y2: the y values for the second subplot
        :returns: the updated figure object
        """
        # for now lets fix it to 2 subplots
        self.n_rows = 2
        self.n_cols = 1

        x = [x1, x2]
        y = [y1, y2]

        y_labels = ["Field (filtered)", "Temp (unfiltered)"]

        # create the subplots with a shared x axis.
        self.fig = make_subplots(rows=self.n_rows,
                                 cols=self.n_cols,
                                 x_title='time',
                                 shared_xaxes=True,
                                 vertical_spacing=0.02,
                                 start_cell='top-left')

        self._height = 900
        self.fig.update_layout(height=self._height)

        # add data to the subplots
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                # plot lines as this is much faster than points
                self.fig.add_trace(plotly.graph_objects.Scatter(
                            x=x[i],
                            y=y[i],
                            name=f'Example plot: {y_labels[i]}',
                            mode='lines'
                            ),
                                  i + 1, j + 1)

                if self._min > np.min(x[i]):
                    self._min = np.min(x[i])

                if self._max < np.max(x[i]):
                    self._max = np.max(x[i])
                self.fig.update_traces(hoverinfo='none')
                self.fig.update_yaxes(title_text=y_labels[i], row=i+1, col=j+1)
        return self.fig


    def display_hover(self, data, filters):
        if data is None:
            return False, no_update, no_update
        pt = data['points'][0]
        bbox = pt['bbox']
        txt = []
        for filter_details in filters:
            if filter_details['Type_t'] == 'Include' and filter_details['Start_t'] <= pt['x'] and filter_details['End_t'] >= pt['x']:
                txt.append(filter_details['Name_t'])
            elif filter_details['Type_t'] == 'Exclude' and (filter_details['Start_t'] >= pt['x'] or filter_details['End_t'] <= pt['x']):
                txt.append(filter_details['Name_t'])


        children = self._view.hover_text(pt, txt)
        return True, bbox, children
