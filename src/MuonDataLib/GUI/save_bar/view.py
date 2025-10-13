from MuonDataLib.GUI.view_template import ViewTemplate
# from MuonDataLib.GUI.utils.my_btn import my_btn
from dash import html
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html


#class my_btn(dbc.Button):
#    def __init__(self, text, name):
#
#        super().__init__(text, id=name, color='primary', className='me-md-2')
#        self.text = text
#        self.name = name
#        callback(Input(self.name, 'n_clicks'),
#                 running=[(Output(self.name, 'children'), [dbc.Spinner(size='sm'), 'doing stuff'], self.text)])(self.load)
#
#    def load(self, n):
#        print("hiiiiii")
#        time.sleep(5)
#        return
#

class SaveBarView(ViewTemplate):

    def generate(self):
        return html.Div([
            #dbc.Button('Moo', id='moo'),
            #my_btn('Moo','moo'),
            dbc.Button('Save', id='Save',
                       color='primary', className='me-md-2'),
            dbc.Button('Save filters', id='save_filters', color='primary',
                       n_clicks=0, className='me-md-2'),

            html.Div(id='save_btn_dummy', children="NONE", hidden=True),
            html.Div(id='save_exe_dummy', children="NONE", hidden=True),
            ],
                        className="d-grid gap-2 d-md-flex "
                                  "justify-content-md-start")

    def set_callbacks(self, presenter):
        return
        #callback(Input('moo', 'n_clicks'),
        #         running=[(Output('moo', 'children'), 'bob', 'moo')])(self.load)

    #def load(self, n):
    #    
    #    time.sleep(5)
    #    return
