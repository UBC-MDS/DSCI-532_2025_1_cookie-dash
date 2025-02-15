from dash import Dash
import dash_bootstrap_components as dbc
from title import title
from ingredient_filter import ingredient_filter
from recipes_info import recipes_info
from recipe_list import recipe_list
from ratings_distribution import ratings_distribution
from recipes_per_ingredient import recipes_per_ingredient

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    title("Cookie Dash"),

    dbc.Row([
        dbc.Col(ingredient_filter(), width=4),
        dbc.Col(recipes_info(), width=4),
        dbc.Col(recipe_list(), width=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(ratings_distribution(), width=6),
        dbc.Col(recipes_per_ingredient(), width=6),
    ], className="mb-4")
], fluid=True)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')