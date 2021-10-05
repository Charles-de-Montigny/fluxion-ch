import dash_bootstrap_components as dbc

from dash import html


class Layout:
    """
    The layout of the app and it describes what the application looks like.
    """
    def __init__(self):
        pass

    def navbar(self):
        navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Vente", href="ds-coach-nhl/team")),
            dbc.NavItem(dbc.NavLink("Marketing", href="ds-coach-nhl/player")),
            dbc.NavItem(dbc.NavLink("Production", href="ds-coach-nhl/field")),
        ],
        brand="DashDev",
        brand_href="ds-coach-nhl",
        sticky="top",
        #color="light",
        dark=True,
        expand="lg",
        )
        return dbc.NavbarSimple(
                    brand="ds-coach-nhl",
                    brand_href="#",
                    color="primary",
                    dark=True,
                    sticky="top",
                )
        return navbar

    def create(self):
        layout = html.Div(
            [self.navbar()]
            )
        return layout