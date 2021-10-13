import plotly.graph_objects as go
import pandas as pd

from dash import html, dcc
from dash_table import DataTable


def bar():
    animals=['giraffes', 'orangutans', 'monkeys']
    fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
    return fig

def player_bar(df: pd.DataFrame, score: str, season: int):
    df.rename(columns={"physical_score": "Physique", "exp_score": "Expérience", "defending_score": "Défense"}, inplace=True)
    df['Offense'] = df[['shooting_score', 'passing_score']].mean(axis=1)
    df.sort_values(score, ascending=False, inplace=True)
    color = {2020: "#a41c2c", 2021:"#041c64"}
    name = {2020: "Saison 2020-21", 2021: "Saison 2021-22"}
    fig = go.Figure(data=[
                        go.Bar(name=name[season],
                            x=df.query(f"season=={season-1}")["name"],
                            y=df.query(f"season=={season-1}")[score],
                            marker_color=color[season]),],
                    layout={"title": f"{score.title()} en vue de la {name[season]}"}
    )
    fig.update_layout(paper_bgcolor="#f8f9fa", plot_bgcolor="#f8f9fa", template="plotly_white",
                      xaxis=dict(tickfont={"size": 16}), title=dict(font={"size": 22}))
    return fig


def comp_player_bar(score: str):
    df = pd.read_csv('data/processed/scores_2021-10-12.csv')
    fig2021 = player_bar(df=df, score=score, season=2021)
    fig2020 = player_bar(df=df, score=score, season=2020)
    return html.Div(children=[dcc.Graph(figure=fig2021), dcc.Graph(figure=fig2020)])


def edition_bar():
    team_score = pd.read_csv("data/processed/team_score.csv", sep=';')
    fig = go.Figure(data=[
        go.Bar(name="Saison 2020-21", x=team_score.query("season==2020")['score'], y=team_score.query("season==2020")['value'], marker_color="#a41c2c",),
        go.Bar(name="Saison 2021-22", x=team_score.query("season==2021")['score'], y=team_score.query("season==2021")['value'], marker_color="#041c64")
    ])
    fig.update_layout(paper_bgcolor="#f8f9fa", plot_bgcolor="#f8f9fa", template="plotly_white", xaxis=dict(tickfont={"size": 18}))
    return fig


def radar(data: pd.DataFrame, joueur_2021: str, joueur_2020: str, players_mapping: dict):
    categories = ['Marqueur', 'Physique', 'Passeur', 'Experience', 'Défensive']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(data.query(f"name=='{joueur_2020}' and season==2019")[
            ['shooting_score', 'physical_score', 'passing_score', 'exp_score', 'defending_score']].values[0]),
        theta=categories,
        fill='toself',
        fillcolor="#041c64",
        opacity=0.55,
        name=players_mapping[joueur_2020] + " - 2020"
    ))
    fig.add_trace(go.Scatterpolar(
        r=list(data.query(f"name=='{joueur_2021}' and season==2020")[
            ['shooting_score', 'physical_score', 'passing_score', 'exp_score', 'defending_score']].values[0]),
        theta=categories,
        fill='toself',
        fillcolor="#a41c2c",
        opacity=0.55,
        name=players_mapping[joueur_2021] + " - 2021"
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                type="linear",
                autotypenumbers="strict",
                autorange=False,
                range=[0, 100],
                angle=90,
                showline=False,
                showticklabels=False,
                ticks="",
            ),
        ),
        #paper_bgcolor="#f8f9fa",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1)
    )

    return fig


def information_table(data: pd.DataFrame, player: str, season: str, players_mapping: dict):
    """
    Generates the information table.
    """
    df = data.query(f"saison=={season} and nom=='{players_mapping[player]}'")
    df = df[['nationalité', 'age', 'tailles', 'poids', 'Repêché']]

    #import pdb; pdb.set_trace()
    table = DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data = df.to_dict("records"),
        style_cell={"textAlign": "center", "font_size": "14px"},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        style_as_list_view=False,
    )
    return table