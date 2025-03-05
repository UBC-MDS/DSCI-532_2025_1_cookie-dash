from dash import html, dcc, callback, Output, Input, State
import pandas as pd

csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    df_recipes = pd.DataFrame(columns=["Recipe_Index", "Complexity_Score", "Rating", 
                                       "Ingredient", "category", "subcategory"])


def ingredient_filter():
    return html.Div(
        id="ingredient-filter-div",
        style={
            "backgroundColor": "#906A51",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row3-start",
            "gridRowEnd": "row6-start",
            "overflowY": "auto"
        },
        children=[
            html.Div(
                style={"width": "100%", "display": "flex"},
                children=[
                    html.Div(
                        style={"width": "66%", "paddingRight": "10px"},
                        children=[
                            html.H4("Available Ingredients"),
                            dcc.Checklist(
                                id="ingredient-checklist",
                                options=[],
                                value=[],  # initially empty
                                style={"display": "block"}
                            ),
                        ]
                    ),
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
    Input('selected-subcategory', 'data'),
    State('ingredient-checklist', 'value')
)
def update_ingredient_checklist(selected_subcat, previously_selected):
    """
    Update the available ingredient options based on the subcategory, but preserve
    any previously selected ingredients so they don't get wiped out when subcategory changes.
    """
    # If no subcategory is picked yet, show all possible ingredients
    if not selected_subcat:
        ingredients = df_recipes["Ingredient"].dropna().unique()
    else:
        # Filter to the new subcategory
        df_sub = df_recipes[df_recipes["subcategory"] == selected_subcat]
        ingredients = df_sub["Ingredient"].dropna().unique()

    # Build new options from these ingredients
    new_options = [{"label": ing, "value": ing} for ing in ingredients]

    # If we want to keep *all* previously selected items (including ones not in this subcat),
    # we can add them to `options` so they remain selectable – so the user can still see them:
    if previously_selected is None:
        previously_selected = []
    # Add any old selection that is not yet in new_options
    old_still_needed = [
        ing for ing in previously_selected
        if ing not in ingredients
    ]
    # That way they don't disappear from the UI
    for old_ing in old_still_needed:
        new_options.append({"label": old_ing, "value": old_ing})

    # The new "value" is just the union of the old selected items
    new_value = previously_selected

    return new_options, new_value


@callback(
    Output('selected-ingredients-list', 'children'),
    Input('ingredient-checklist', 'value')
)
def show_selected_ingredients(selected_ingredients):
    if not selected_ingredients:
        return [html.Li("No ingredients selected")]

    return [html.Li(ing) for ing in selected_ingredients]