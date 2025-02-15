import dash_bootstrap_components as dbc
from dash import html

def recipes_info(title="Recipes Info"):
    return dbc.Row(
        dbc.Col(
            html.Div(title, className="text-center p-4 border"),
            width=12
        ),
        className="mb-4"
    )