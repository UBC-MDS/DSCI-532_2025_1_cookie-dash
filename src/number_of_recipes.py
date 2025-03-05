""" from dash import html

def number_of_recipes():
    return html.Div(
        "Number of Recipes",
        className="number_of_recipes",
        style={
            "backgroundColor": "#90ee90",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col8-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row4-start"
        }
    ) """

from dash import html, callback, Output, Input
import pandas as pd

# Load data
csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    # Create empty DataFrame if CSV is missing
    df_recipes = pd.DataFrame(columns=["Recipe_Index", "Rating", "Ingredient"])

def number_of_recipes():
    """
    Displays the number of recipes, updating dynamically based on filters.
    """
    return html.Div(
        id="recipe-count-container",
        children=[
            html.H4("Number of Recipes"),
            html.H2(id="recipe-count", children="0")  # ✅ Updated dynamically
        ],
        className="number_of_recipes",
        style={
            "backgroundColor": "#D2A679",
            "color": "#000",
            "padding": "20px",
            "textAlign": "center",
            "borderRadius": "5px",
            "boxShadow": "2px 2px 5px rgba(0, 0, 0, 0.3)",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col8-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row4-start"
        }
    )

@callback(
    Output("recipe-count", "children"),
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value")  # ✅ Added ingredient selection as an input
)
def update_recipe_count(rating_range=[0, 1], selected_ingredients=None):
    """
    Updates the displayed count of recipes based on rating range and selected ingredients.
    """
    # Filter by rating range
    filtered_df = df_recipes[df_recipes["Rating"].between(rating_range[0], rating_range[1])]

    # If ingredients are selected, filter by them
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    # Count unique recipes
    num_recipes = filtered_df["Recipe_Index"].nunique()

    return f"{num_recipes}"
