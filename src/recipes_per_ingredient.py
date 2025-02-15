import dash_bootstrap_components as dbc
from dash import html

def recipes_per_ingredient(title="Recipes per Ingredient"):
    return dbc.Row(
        dbc.Col(
            html.Div(title, className="text-center p-4 border"),
            width=12
        ),
        className="mb-4"
    )