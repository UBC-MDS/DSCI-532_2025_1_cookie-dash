from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask_caching import Cache

# Import component functions
from .components import *
from . import callbacks
from os import path as os_path

PREFIX = '/'

app = Dash(
    __name__,
    routes_pathname_prefix=PREFIX,
    requests_pathname_prefix=PREFIX,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server

cache = Cache(
    server,
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'tmp'
    }
)

# Layout mimicking the original HTML structure
app.layout = html.Div(
    className="content",
    children=[
        dcc.Store(id='selected-subcategory', storage_type='memory'),
        header(),
        html.Main(
            children=[
                html.Div(
                    className="grid",
                    children=[
                        ingredient_icons(),
                        ingredient_filter(),
                        distribution_recipe_ratings(),
                        average_rating(),
                        number_of_recipes_per_ingredient(),
                        recipes_and_complexity()
                    ],
                    style={
                        "display": "grid",
                        "gridTemplateColumns": (
                            "[col1-start] 1fr [col2-start] 1fr [col3-start] 1fr [col4-start] 1fr [col5-start] 1fr "
                            "[col6-start] 1fr [col7-start] 1fr [col8-start] 1fr [col9-start] 1fr [col10-start] 1fr [col11-end]"
                        ),
                        "gridTemplateRows": (
                            "[row1-start] 1fr [row2-start] 1fr [row3-start] 1fr [row4-start] 1fr "
                            "[row5-start] 1fr [row6-start] 1fr [row7-start] 1fr [row8-start] 1fr [row9-end]"
                        ),
                        "height": "80vh",
                        "gap": "1vw",
                        "margin": "0 5vw",
                    }
                )
            ]
        ),
        footer()
    ],
    style={
        "backgroundColor": "#F5E1C8",
    }
)

if __name__ == '__main__':
    app.run_server()