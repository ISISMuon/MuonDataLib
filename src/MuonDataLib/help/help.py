from MuonDataLib.help.help_docs import _text, tags

from dash import Dash, Input, Output, callback, dcc, html, State
import dash_bootstrap_components as dbc


def help_app():
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(
        [
            html.H4(
                "MuonDataLib API doc",
                style={"textAlign": "center"},
                className="mb-3",
            ),
            # ------------------------------------------------- #
            # Modal
            html.Div(
                [
                    dbc.Button("Open filters", id="open", n_clicks=0),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Filters")),
                            dbc.ModalBody(
                                [
                                    # Filter within dbc Modal
                                    html.Label("Tag"),
                                    dcc.Dropdown(
                                        id="dynamic_callback_dropdown_region",
                                        options=[
                                            {"label": x, "value": x}
                                            for x in tags
                                        ],
                                        multi=True,
                                    ),
                                ]
                            ),
                        ],
                        id="modal",
                        is_open=False,
                    ),
                ],
                className="mb-5",
            ),
            dcc.Markdown('''
                #### Dummy text
                production baby: Melody Lim
            ''', id='text'),
            html.Div(id="tabs-content"),
        ],
        fluid=True,
    )

    def get_text(val, tags):
        for t in tags:
            if t not in val.tags:
                return ''
        return val.get_MD()

    @callback(
        Output("text", "children"),
        Input("dynamic_callback_dropdown_region", "value"),
    )
    def main_callback_logic(region):
        if region is None:
            a = ''
            for key in _text:
                a += key.get_MD() + '''\n'''
            return a.strip("'")
        a = ''
        for key in _text:
            a += get_text(key, region)
        return a.strip("'")

    @callback(
        Output("modal", "is_open"),
        Input("open", "n_clicks"),
        State("modal", "is_open"),
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open

    return app
