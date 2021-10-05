# -*- coding: utf-8 -*-
import os

import dash
import dash_auth
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from dash import html, dcc
from dash.dependencies import Input, Output


from src.layout import Layout

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

app = dash.Dash(
    __name__,
    external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
                          dbc.themes.SUPERHERO],
    title="ds-coach-nhl",
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

# Auth
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Describe the layout/ UI of the app
app.layout = Layout().create()
server = app.server

# Callbacks


if __name__ == "__main__":
    app.run_server(debug=debug, dev_tools_hot_reload=True, port=8181)
