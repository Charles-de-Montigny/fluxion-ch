import plotly.graph_objects as go
import pandas as pd

from dash_table import DataTable


def bar():
    animals=['giraffes', 'orangutans', 'monkeys']
    fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
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