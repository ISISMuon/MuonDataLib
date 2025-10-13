from MuonDataLib.GUI.view_template import ViewTemplate
from dash import html


class FilterView(ViewTemplate):

    def generate(self):
        return html.Div([
            html.H3("Title: testing", id='title_test'),
            ])

    def set_callbacks(self, presenter):
        return
