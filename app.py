# -*- coding: utf-8 -*-
import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dotenv import load_dotenv
from dash import html, dcc
from dash.dependencies import Input, Output

from src.viz import radar, information_table, comp_player_bar
from src.layout import Layout
from src.utils import read_json
from src.base import footer, navbar

# Setup
if not os.environ.get("ADMIN"):
    load_dotenv()
    debug = True
else:
    debug = False

# Load data
scores = pd.read_csv("data/processed/scores_2021-10-12.csv")
info_table = pd.read_csv("data/processed/players_info.csv", sep=";")

app = dash.Dash(
    __name__,
    external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
                          dbc.themes.BOOTSTRAP],
    title="Fluxion-CH",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

# Describe the layout/ UI of the app
app.layout = html.Div(children=[
    dcc.Location(id="url"),
    html.Div(id='page-content')
])

server = app.server

# Callbacks
@app.callback(
    Output(component_id="page-content", component_property="children"),
    Input(component_id="url", component_property="pathname")
)
def display_page(pathname):
    if pathname == "/":
        return Layout("joueurs", scores, footer, navbar).create()
    return Layout(pathname.replace("/", ""), scores, footer, navbar).create()

@app.callback(
    Output(component_id="player_score", component_property="children"),
    Input(component_id="dd_score", component_property="value")
)
def update_player_bar(score):
    return comp_player_bar(score)


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
    Output(component_id='info_table_2020', component_property='children'),
    Input(component_id='dd_2020', component_property='value')
)
def update_table_2020(name):
    players = read_json("config/players.json")
    players_mapping = {player.replace(" ", "").lower(): player
                       for player in set(players['2020'] + players['2021'])}
    return information_table(data=info_table, player=name, season=2020,
                             players_mapping=players_mapping)


@app.callback(
    Output(component_id='info_table_2021', component_property='children'),
    Input(component_id='dd_2021', component_property='value')
)
def update_table_2020(name):
    players = read_json("config/players.json")
    players_mapping = {player.replace(" ", "").lower(): player
                       for player in set(players['2020'] + players['2021'])}
    return information_table(data=info_table, player=name, season=2021,
                             players_mapping=players_mapping)


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
    scores = pd.read_csv("data/processed/scores_2021-10-12.csv")
    scores['name'] = scores['name'].apply(lambda x: x.replace(" ", "").lower())
    players = read_json("config/players.json")
    players_mapping = {player.replace(" ", "").lower(): player
                       for player in set(players['2020'] + players['2021'])}
    return dcc.Graph(figure=radar(data=scores,
                                  joueur_2021=joueur_2021,
                                  joueur_2020=joueur_2020,
                                  players_mapping=players_mapping), className="radar_graph", config={
        'displayModeBar': False
    })



if __name__ == "__main__":
    app.run_server(debug=False, dev_tools_hot_reload=True, port=8180)
