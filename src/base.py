from dash import html
import dash_bootstrap_components as dbc


navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/img/ch.svg", className="ch"), className="ch"),
                        dbc.Col(html.Img(src="assets/img/gohabsgo.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand(html.A(html.Strong("Joueurs"), href="joueurs"), className="ml-2 navheader", external_link="/joueurs")),
                        dbc.Col(dbc.NavbarBrand(html.A(html.Strong("Équipes"), href='equipes'), className="ml-2 navheader", external_link="/")),
                        dbc.Col(dbc.NavbarBrand(html.A(html.Strong("Méthodologie"), href="methodologie"), className="ml-2 navheader", external_link="/")),
                    ],
                    align="center",
                    no_gutters=True,
                )
            )
        ],
        color="#041c64",
        dark=True,
        sticky='top',   
        className="navbar-top")


footer = html.Div(className="footer", children=[
    html.Footer(className="text-center text-lg-start bg-light text-muted"),
    html.Section(children=[
        html.Div(children=[html.Span("")], className="me-5 d-none d-lg-block"),
        html.Div(children=[
            html.A(href="https://www.linkedin.com/in/charles-demontigny/", className='fab fa-linkedin'),
            html.A(href="https://github.com/DS-Coach", className="fab fa-github")],
        className="me-4 text-reset")
    ],
        className="d-flex justify-content-center justify-content-lg-between p-4 border-bottom"),
    html.Section(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H6(children=[html.I(className="fas fa-gem me-3"), "Fluxion"], className="text-uppercase fw-bold mb-4"),
                    html.P("""Entreprise de développement logiciel spécialisée en science des données et en analytique d'affaires.""")
                ], className="col-md-3 col-lg-4 col-xl-3 mx-auto mb-4"),
                html.Div(children=[
                    html.H6(children=[html.I(className="fas fa-gem me-3"), "Produits"], className="text-uppercase fw-bold mb-4"),
                    html.P("""Fluxion crée des tableaux de bords personnalisés pour ses clients.""")
                ], className="col-md-2 col-lg-2 col-xl-2 mx-auto mb-4"),
                html.Div(children=[
                    html.H6(children=[html.I(className="fas fa-gem me-3"), "Contact"], className="text-uppercase fw-bold mb-4"),
                    html.P(children=[html.A("Montréal, Québec", href="https://www.google.com/maps/place/Montr%C3%A9al,+QC/@45.5579564,-73.8703843,11z/data=!3m1!4b1!4m5!3m4!1s0x4cc91a541c64b70d:0x654e3138211fefef!8m2!3d45.5016889!4d-73.567256")]),
                    html.P(children=[html.A("info@fluxion.ca", href=""), ]),
                    html.P(children=html.A("LinkedIn", href='https://www.linkedin.com/in/charles-demontigny/'))
                ], className="col-md-2 col-lg-2 col-xl-2 mx-auto mb-4")
            ], className="row mt-3")
        ], className="container text-center text-md-start mt-5"),
        
    ]),

])