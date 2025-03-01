from dash import Dash, html
import dash_bootstrap_components as dbc

# Import component functions
from header import header
from footer import footer
from ingredient_icons import ingredient_icons
from ingredient_filter import ingredient_filter
from distribution_recipe_ratings import distribution_recipe_ratings
from number_of_recipes import number_of_recipes
from average_rating import average_rating
from number_of_recipes_per_ingredient import number_of_recipes_per_ingredient
from recipes_and_complexity import recipes_and_complexity, update_recipe_list

# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout mimicking the original HTML structure
app.layout = html.Div(
    className="content",
    children=[
        header(),
        html.Main(
            children=[
                html.Div(
                    className="grid",
                    children=[
                        ingredient_icons(),
                        ingredient_filter(),
                        distribution_recipe_ratings(),
                        number_of_recipes(),
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
                        "height": "85vh",
                        "gap": "1vw",
                        "margin": "0 5vw"
                    }
                )
            ]
        ),
        footer()
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')