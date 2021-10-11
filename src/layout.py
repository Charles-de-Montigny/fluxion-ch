from typing import List

import dash_bootstrap_components as dbc

import pandas as pd
from dash import html, dcc
from dash_table import DataTable

from src.viz import radar, bar


def sidebar():
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "14rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    sidebar = html.Div(
        [
            #html.H2("Sidebar", className="display-4"),
            html.Img(src="assets/img/ch.png", height="200px", width="300px"),
            html.Hr(),
            html.H3("Canadiens de Montréal"),
            #html.H6(
            #    "Saison 2021-2022", className="lead"
            #),
            #dbc.Nav(
            #    [
            #        dbc.NavLink("Home", href="/", active="exact"),
            #        dbc.NavLink("Page 1", href="/page-1", active="exact"),
            #        dbc.NavLink("Page 2", href="/page-2", active="exact"),
            #    ],
            #    vertical=True,
            #    pills=True,
            #),
        ],
        style=SIDEBAR_STYLE,
    )
    return sidebar


# padding for the page content
CONTENT_STYLE = {
    "padding": "2rem 1rem",
}

info_player = [
    "short_name",
    "nationality",
    "club_name",
    "age",
    "height_cm",
    "weight_kg",
]
labels_table = ["Player", "Nationality", "Club", "Age", "Height (cm)", "Weight (kg)"]

df = pd.DataFrame({"short_name": "Jeff Petry", "nationality": "Canadien",
                   "club_name": "Canadiens", "age": 32, "height_cm": 180, "weight_kg": 180}, index=[0])

player_table = DataTable(
    columns=[
        {"name": col, "id": info_player[idx]} for (idx, col) in enumerate(labels_table)
    ],
    data=df.to_dict("records"),
    style_cell={"textAlign": "left", "font_size": "14px"},
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

player_info_card = dbc.Card(
                        dbc.CardBody([
                            html.Div("Position"),
                            html.Div("Center")
                        ]),
                        className="box"
                    )

player_card_ = dbc.Container(
        dbc.Col(
            dbc.Card(
                children=[
                    dbc.Row(
                        player_table
                    ),
                    dbc.Row(
                        dbc.CardDeck(
                            children=[
                                player_info_card,
                                player_info_card,
                                player_info_card,
                                player_info_card
                            ]
                        )
                    )
                ]
            ), 
        width=5), 
    fluid=True)


class Layout:
    """
    The layout of the app and it describes what the application looks like.
    """
    def __init__(self, scores: pd.DataFrame) -> None:
        self.scores = scores

    def navbar(self):
        #return sidebar()
        nav = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/img/ch.svg", className="ch"), className="ch"),
                        dbc.Col(html.Img(src="assets/img/gohabsgo.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand(html.Strong("Joueurs"), className="ml-2 navheader", external_link="/")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="#",
            )
        ],
        color="#041c64",
        dark=True,
        sticky='top',   
        style={"height": "100px", "width":"100%"})
        return nav

    def dropdown(self, players: List[str], year: int, default: str):
        """
        Dropdown.
        """
        return dcc.Dropdown(
            id=f'dd_{year}',
            options=[
                {'label': player, 'value': player.replace(" ", "").lower()}
                for player in players],
            value=default
        )

    def body(self):
        return html.Div(
            [   # Row 1
                dbc.Row(
                    dbc.Col(
                        dbc.Container(children=[
                                html.H1(html.Strong("Comparaison des joueurs: 2021-22 Vs. 2020-21")),
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
                                    html.H3("Joueurs 2021-22"),
                                    self.dropdown(players=self.scores.query("season==2020")['name'], year=2021, default='christiandvorak'),
                                    dbc.Container(html.Div(id="photo_2021"), fluid=True)
                                ]
                            ), className="w-100 box",
                            ), width=3),
                            # Row 1 Col 2
                            dbc.Col(dbc.Card(
                                children=dbc.CardBody(
                                    id="radar"
                                ), className="box"
                            ), width=6),
                            # Row 1 Col 3
                            dbc.Col(dbc.Card(
                                children = dbc.CardBody([
                                    html.H3("Joueurs 2020-21"),
                                    self.dropdown(players=self.scores.query("season==2019")['name'], year=2020, default='jesperikotkaniemi'),
                                    dbc.Container(html.Div(id="photo_2020"), fluid=True)
                                ]), className="box"
                            ), width=3),
                        ]))
                    
                ),
                # Row 3
                dbc.Row(
                    children=[
                        dbc.Container(fluid=True,  children=[
                            # Information Table
                            dbc.CardDeck(children=[
                                dbc.Card([
                                    dbc.CardBody([player_table]),
                                    dbc.Container(
                                        dbc.CardDeck(
                                        [player_info_card,
                                         player_info_card,
                                         player_info_card,
                                         player_info_card],
                                         className="info_card"
                                        )
                                    ),
                                    dbc.Container(fluid=True,
                                        children=[dcc.Graph(figure=bar())]
                                    ),
                                    html.Br()
                                ], className="box"), 
                                dbc.Card([
                                    dbc.CardBody([player_table]),
                                    dbc.Container(
                                        dbc.CardDeck(
                                        [player_info_card,
                                         player_info_card,
                                         player_info_card,
                                         player_info_card],
                                         className="info_card"
                                        )
                                    ),
                                    dbc.Container(fluid=True,
                                        children=[dcc.Graph(figure=bar())]
                                    ),
                                    html.Br()
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
                self.navbar(),
                self.body(),
                html.Div(id="page-content", children=[], style=CONTENT_STYLE),
            ]
            )
        return layout