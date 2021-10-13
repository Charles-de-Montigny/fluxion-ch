from typing import List

import dash_bootstrap_components as dbc

import pandas as pd
from dash import html, dcc
from dash_table import DataTable

from src.viz import edition_bar, comp_player_bar



# padding for the page content
CONTENT_STYLE = {
    "padding": "2rem 1rem",
}





player_info_card = dbc.Card(
                        dbc.CardBody([
                            html.Div("Position"),
                            html.Div("Center")
                        ]),
                        className="info_card"
                    )


class Layout:
    """
    The layout of the app and it describes what the application looks like.
    """
    def __init__(self, page: str, scores: pd.DataFrame, footer, navbar) -> None:
        self.scores = scores
        self.footer = footer
        self.navbar = navbar
        self.page = page

    def dropdown(self, players: List[str], year: int, default: str):
        """
        Dropdown.
        """
        return dcc.Dropdown(
            id=f'dd_{year}',
            options=[
                {'label': player, 'value': player.replace(" ", "").lower()}
                for player in players],
            value=default,
            searchable=False,
            clearable=False
        )

    def dd_score(self):
        scores = ["Offense", "Défense", 'Physique', 'Expérience']
        return dcc.Dropdown(
            id=f'dd_score',
            options=[{'label': score, 'value': score} for score in scores],
            value="Offense",
            searchable=False,
            clearable=False,
            className="dd_score"
        )

    def body(self):
        if self.page == 'equipes':
            return html.Div(children=[
                dbc.Container(children=[
                    html.Br(),
                    html.H1(html.Strong("Comparaison des Équipes"), className='titreequipe'),
                    html.Hr(),
                    html.Br(),
                    html.H2(html.Strong("Édition 2021-22 Vs. 2020-21"), className='titreequipe'),
                    dcc.Graph(figure=edition_bar(), config={'displayModeBar': False}),
                    html.Hr(),
                    self.dd_score(),
                    html.Div(id="player_score"),
                    html.Br()
                ])
                
            ], className="page")
        if self.page == "methodologie":
            return html.Div(children=[
                dbc.Container([
                    html.H1(html.Strong("Méthodologie")),
                    html.Hr(),
                    html.H2("Source des données"),
                    dcc.Markdown('''
                    * MoneyPuck.com
                    * NHL.com
                    * HockeyDB.com

                    *Les détails méthodologiques sont à venir.*
                    ''', className='markdown')
                ]
                )
            ], className="page", style=CONTENT_STYLE,)
        if self.page == "joueurs":
            return html.Div(
                [   # Row 1
                    dbc.Row(
                        dbc.Col(
                            dbc.Container(children=[
                                    html.H1(html.Strong("Comparaison des joueurs")),
                                    html.Hr()
                                ], 
                                fluid=True),
                            width=12
                        ), className="title"
                    ),
                    # Row 2
                    dbc.Row(
                        children=dbc.Container(fluid=True,  children=
                        
                            dbc.Row([   # Row 1 Col 1
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H3("Éditions 2021-22"),
                                        self.dropdown(players=self.scores.query("season==2020")['name'], year=2021, default='christiandvorak'),
                                        dbc.Container(html.Div(id="photo_2021"), fluid=True)
                                    ]
                                ), className="w-100 box",
                                ), width=3),
                                # Row 1 Col 2
                                dbc.Col(dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                        id="radar"
                                    )], className="box"
                                ), width=6),
                                # Row 1 Col 3
                                dbc.Col(
                                    dbc.Card(
                                        children = dbc.CardBody([
                                            html.H3("Éditions 2020-21"),
                                            self.dropdown(players=self.scores.query("season==2019")['name'], year=2020, default='jesperikotkaniemi'),
                                            dbc.Container(html.Div(id="photo_2020"), fluid=True)
                                        ]), className="box"
                                ), width=3, style={"height": "100%"}),
                            ]))
                        
                    ),
                    # Row 3
                    dbc.Row(
                        children=[
                            dbc.Container(fluid=True,  children=[
                                # Information Table
                                dbc.CardDeck(children=[
                                    dbc.Card([
                                        dbc.CardBody(id="info_table_2021")
                                    ], className="box"), 
                                    dbc.Card([
                                        dbc.CardBody(id="info_table_2020"),
                                    ], className="box")
                                ])
                            ])
                        ]
                    )

                    
                ],
                style=CONTENT_STYLE,
                className="page"
            ) 

    def create(self):
        layout = html.Div(
            [
                self.navbar,
                self.body(),
                self.footer
            ]
            )
        return layout