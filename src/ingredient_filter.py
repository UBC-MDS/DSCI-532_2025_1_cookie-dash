from dash import html, callback, Output, Input
import pandas as pd

csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    # Create empty DataFrame with expected columns if CSV not found
    df_recipes = pd.DataFrame(
        columns=["Recipe_Index", "Complexity_Score", "Rating", "Ingredient", "category", "subcategory"]
    )

def ingredient_filter():
    return html.Div(
        id="ingredient-filter-div",
        style={
            "backgroundColor": "#d3d3d3",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row3-start",
            "gridRowEnd": "row6-start",
            "overflowY": "auto"
        },
        children=["Ingredient Filter"]  # Default text
    )

@callback(
    Output('ingredient-filter-div', 'children'),
    Input('selected-subcategory', 'data')
)
def update_ingredient_filter(selected_subcat):
    if not selected_subcat:
        return "Select a subcategory above to see ingredients."

    df = df_recipes[df_recipes["subcategory"] == selected_subcat]

    ingredients = df["Ingredient"].dropna().unique()
    if len(ingredients) == 0:
        return f"No ingredients found for subcategory: {selected_subcat}"

    return html.Ul([html.Li(ing) for ing in ingredients])