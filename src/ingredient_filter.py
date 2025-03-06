from dash import html, dcc, callback, Output, Input, State, callback_context
import dash_bootstrap_components as dbc
import pandas as pd

csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    df_recipes = pd.DataFrame(
        columns=["Recipe_Index", "Complexity_Score", "Rating", 
                 "Ingredient", "category", "subcategory", "Popularity_Score"]
    )

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
            "borderRadius": "5px",
            "overflowY": "auto",
            "border": "2px solid #906A51",
        },
        children=[
            html.Div(
                style={"width": "100%", "display": "flex"},
                children=[
                    # Left side: Available Ingredients title with header row and checklist
                    html.Div(
                        style={"width": "66%", "paddingRight": "10px"},
                        children=[
                            html.Div(
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center"
                                },
                                children=[
                                    html.H4("Available Ingredients", style={"margin": 0}),
                                    dbc.Button(
                                        "Deselect All",
                                        id="deselect-all-button",
                                        n_clicks=0,
                                        style={"marginLeft": "10px"}
                                    )
                                ]
                            ),
                            # Header row for columns
                            html.Div(
                                children=[
                                    html.Span("Ingredient", style={"flex": "1", "textAlign": "left"}),
                                    html.Span("Popularity Score", style={"minWidth": "50px", "textAlign": "right"})
                                ],
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center",
                                    "fontWeight": "bold",
                                    "padding": "4px 8px",
                                    "borderBottom": "1px solid #ccc",
                                    "marginTop": "10px"
                                }
                            ),
                            # Checklist with custom label styling so checkbox and label share the same row.
                            dcc.Checklist(
                                id="ingredient-checklist",
                                options=[],  # options are generated in the callback below
                                value=[],    # initially no ingredient is selected
                                labelStyle={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center",
                                    "width": "100%",
                                    "padding": "4px 8px"
                                },
                                style={"display": "block", "marginTop": "5px"}
                            )
                        ]
                    ),
                    # Right side: Selected Ingredients (only names)
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
    Input('deselect-all-button', 'n_clicks'),
    State('ingredient-checklist', 'value')
)
def update_ingredient_checklist(selected_subcat, n_clicks_deselect, previously_selected):
    ctx = callback_context
    # If "Deselect All" was clicked, clear the selected ingredients.
    if ctx.triggered and 'deselect-all-button' in ctx.triggered[0]['prop_id']:
        new_value = []
    else:
        new_value = previously_selected if previously_selected is not None else []

    # Filter ingredients by subcategory if provided.
    if not selected_subcat:
        ingredients = df_recipes["Ingredient"].dropna().unique()
    else:
        df_sub = df_recipes[df_recipes["subcategory"] == selected_subcat]
        ingredients = df_sub["Ingredient"].dropna().unique()

    new_options = []
    # Build options with a two-column label: ingredient name on left, popularity score on right.
    for ing in ingredients:
        pop_series = df_recipes[df_recipes["Ingredient"] == ing]["Popularity_Score"]
        pop_score = round(pop_series.mean() if not pop_series.empty else 0.00, 2)
        label = html.Div(
            [
                html.Span(ing, style={"flex": "1", "textAlign": "left"}),
                html.Span(str(pop_score), style={"minWidth": "50px", "textAlign": "right"})
            ],
            style={"display": "flex", "justifyContent": "space-between", "width": "100%"}
        )
        new_options.append({"label": label, "value": ing})

    # Preserve any previously selected ingredient not in the current subcategory.
    if not (ctx.triggered and 'deselect-all-button' in ctx.triggered[0]['prop_id']):
        old_still_needed = [ing for ing in new_value if ing not in ingredients]
        for old_ing in old_still_needed:
            pop_series = df_recipes[df_recipes["Ingredient"] == old_ing]["Popularity_Score"]
            pop_score = round(pop_series.mean() if not pop_series.empty else 0.0, 1)
            label = html.Div(
                [
                    html.Span(old_ing, style={"flex": "1", "textAlign": "left"}),
                    html.Span(str(pop_score), style={"minWidth": "50px", "textAlign": "right"})
                ],
                style={"display": "flex", "justifyContent": "space-between", "width": "100%"}
            )
            new_options.append({"label": label, "value": old_ing})
    
    return new_options, new_value

@callback(
    Output('selected-ingredients-list', 'children'),
    Input('ingredient-checklist', 'value')
)
def show_selected_ingredients(selected_ingredients):
    if not selected_ingredients:
        return [html.Li("No ingredients selected")]
    return [html.Li(ing) for ing in selected_ingredients]