# -*- coding: utf-8 -*-
import os

import dash
import dash_auth
import dash_bootstrap_components as dbc
import pandas as pd
from dotenv import load_dotenv
from dash import html, dcc
from dash.dependencies import Input, Output

from src.viz import radar
from src.layout import Layout
from src.utils import read_json

# Setup
if not os.environ.get("ADMIN"):
    load_dotenv()
    debug = True
else:
    debug = False

# Credentials
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': os.environ.get("ADMIN"),
    'dev': "DO_NOT_LEAVE_THIS_PASSWORD"
}

# Load data
scores = pd.read_csv("data/processed/scores.csv")

app = dash.Dash(
    __name__,
    external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
                          dbc.themes.BOOTSTRAP],
    title="ds-coach-nhl",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

# Auth
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Describe the layout/ UI of the app
app.layout = Layout(scores).create()
server = app.server

# Callbacks
@app.callback(
    Output(component_id='photo_2021', component_property='children'),
    Input(component_id='dd_2021', component_property='value')
    )
def update_photo2021(name):
    """
    Photo 2021.
    """
    return html.Img(src=f"assets/img/players/{name}.jpeg",
                    #height="405px",
                    #width="375px",
                    className="img")


@app.callback(
    Output(component_id='photo_2020', component_property='children'),
    Input(component_id='dd_2020', component_property='value')
    )
def update_photo2020(name):
    """
    Photo 2020.
    """
    return html.Img(src=f"assets/img/players/{name}.jpeg",
                    #height="405px",
                    #width="375px",
                    className="img")


@app.callback(
    Output(component_id="radar", component_property="children"),
    [Input(component_id="dd_2021", component_property="value"),
     Input(component_id="dd_2020", component_property="value")])
def update_radar(joueur_2021, joueur_2020):
    scores = pd.read_csv("data/processed/scores.csv")
    scores['name'] = scores['name'].apply(lambda x: x.replace(" ", "").lower())
    players = read_json("config/players.json")
    players_mapping = {player.replace(" ", "").lower(): player
                       for player in set(players['2020'] + players['2021'])}
    return dcc.Graph(figure=radar(data=scores,
                                  joueur_2021=joueur_2021,
                                  joueur_2020=joueur_2020,
                                  players_mapping=players_mapping), className="radar_graph")



if __name__ == "__main__":
    app.run_server(debug=debug, dev_tools_hot_reload=True, port=8080)
