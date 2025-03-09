from dash import callback, Output, Input, State, callback_context, ALL, html
import pandas as pd
import ast
import altair as alt
import json

# ingredient icons callbacks
csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    # Create empty DataFrame with expected columns if CSV not found
    df_recipes = pd.DataFrame(
        columns=["Recipe_Index", "Complexity_Score", "Rating", "Ingredient", "category", "subcategory"]
    )

@callback(
    Output('selected-subcategory', 'data'),
    Input({'type': 'subcategory-button', 'index': ALL}, 'n_clicks')
)
def update_selected_subcategory(n_clicks_list):
    ctx = callback_context
    if not ctx.triggered or sum(n_clicks_list) == 0:
        return df_recipes["Ingredient"].dropna().unique().tolist()
    triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
    triggered_id = ast.literal_eval(triggered_id_str)
    return triggered_id['index']

@callback(
    Output({'type': 'subcategory-button', 'index': ALL}, 'active'),
    Input('selected-subcategory', 'data'),
    State({'type': 'subcategory-button', 'index': ALL}, 'id')
)
def update_active_buttons(selected_subcat, ids):
    return [id_dict['index'] == selected_subcat for id_dict in ids]

# ingredient filter callbacks
try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    df_recipes = pd.DataFrame(
        columns=["Recipe_Index", "Complexity_Score", "Rating", 
                 "Ingredient", "category", "subcategory", "Popularity_Score"]
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

# distribution recipe ratings callbacks to update x-axis based on slider values
df = pd.read_csv("data/processed/processed_cookie_data.csv")

@callback(
    Output("rating_histogram", "spec"),
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value"),
)
def create_ratings_distribution(rating_range=[0, 1], selected_ingredients=None):
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    # group by recipe ID so that there is only one entry per recipe instead of per ingredient in the recipe
    # the recipe's rating per ingredient should be the same, so "mean" doesn't really do anything
    filtered_df = filtered_df.groupby("Recipe_Index")['Rating'].mean().reset_index()


    chart = alt.Chart(filtered_df).mark_bar().encode(
        alt.X("Rating:Q", bin=alt.Bin(maxbins=10),
              title="Rating",
              scale=alt.Scale(domain=rating_range),
              axis=alt.Axis(domainColor="#3E2723", tickColor='#3E2723')
              ),
        alt.Y("count():Q",
              title="Count",
              axis=alt.Axis(gridColor='#D2A679', domainColor="#3E2723", tickColor='#3E2723')
              ),
        tooltip=[alt.Tooltip("count():Q", title="Number of Recipes")],
        color=alt.value('#906A51')
    ).properties(width="container", height = "container"
    ).configure(background='#F5E1C8').configure_view(strokeWidth=0)

    return (chart.to_dict())

# number of recipes callback
try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    # Create empty DataFrame if CSV is missing
    df_recipes = pd.DataFrame(columns=["Recipe_Index", "Rating", "Ingredient"])

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