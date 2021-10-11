import plotly.graph_objects as go
import pandas as pd


def bar():
    animals=['giraffes', 'orangutans', 'monkeys']
    fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
    return fig


def radar(data: pd.DataFrame, joueur_2021: str, joueur_2020: str, players_mapping: dict):
    categories = ['Shooting', 'Physical', 'Passing']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(data.query(f"name=='{joueur_2020}' and season==2019")[
            ['shooting_score', 'physical_score', 'passing_score']].values[0]),
        theta=categories,
        fill='toself',
        name=players_mapping[joueur_2020] + " - 2020"
    ))
    fig.add_trace(go.Scatterpolar(
        r=list(data.query(f"name=='{joueur_2021}' and season==2020")[
            ['shooting_score', 'physical_score', 'passing_score']].values[0]),
        theta=categories,
        fill='toself',
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
        paper_bgcolor="#f8f9fa",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1)
    )


    return fig