from dash import html, dcc, callback, Output, Input
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
            # Keep scroll if you expect lots of items:
            "overflowY": "auto"
        },
        children=[
            # We'll place two "columns" within this parent DIV
            
            html.Div(
                style={"width": "100%", "display": "flex"},
                children=[
                    # Left 2/3 column: Checklist for ingredients
                    html.Div(
                        style={"width": "66%", "paddingRight": "10px"},
                        children=[
                            html.H4("Available Ingredients"),
                            dcc.Checklist(
                                id="ingredient-checklist",
                                options=[],
                                value=[],  # start empty
                                style={"display": "block"}  # items on their own lines
                            ),
                        ]
                    ),
                    # Right 1/3 column: Display selected ingredients
                    html.Div(
                        style={"width": "34%", "paddingLeft": "10px", "borderLeft": "1px solid #aaa"},
                        children=[
                            html.H4("Selected Ingredients"),
                            html.Ul(id="selected-ingredients-list", children=[])
                        ]
                    )
                ]
            )
        ]
    )

@callback(
    Output('ingredient-checklist', 'options'),
    Output('ingredient-checklist', 'value'),
    Input('selected-subcategory', 'data')
)
def update_ingredient_checklist(selected_subcat):
    """
    1) Update the checklist `options` whenever a subcategory is selected.
    2) Reset the `value` (selected items) to empty each time subcategory changes.
    """
    if not selected_subcat:
        # Show all unique ingredients if no subcategory is selected
        ingredients = df_recipes["Ingredient"].dropna().unique()
    else:
        # Show only ingredients from the selected subcategory
        df = df_recipes[df_recipes["subcategory"] == selected_subcat]
        ingredients = df["Ingredient"].dropna().unique()

    if len(ingredients) == 0:
        return [{"label": "No ingredients available", "value": ""}], []

    # Build list of label/value pairs for the Checklist
    options = [{"label": ing, "value": ing} for ing in ingredients]

    # Reset the selection to an empty list each time subcategory changes
    return options, []

@callback(
    Output('selected-ingredients-list', 'children'),
    Input('ingredient-checklist', 'value')
)
def show_selected_ingredients(selected_ingredients):
    """
    For each selected ingredient, create a <li> in an unordered list.
    If none are selected, display a simple message.
    """
    if not selected_ingredients:
        return [html.Li("No ingredients selected")]

    return [html.Li(ing) for ing in selected_ingredients]