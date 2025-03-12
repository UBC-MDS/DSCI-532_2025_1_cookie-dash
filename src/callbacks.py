from dash import callback, Output, Input, State, callback_context, ALL, html
import dash_bootstrap_components as dbc
import pandas as pd
import ast
import altair as alt
import json
import plotly.graph_objects as go
from .app import cache

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
@cache.memoize()
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
@cache.memoize()
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
@cache.memoize()
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
@cache.memoize()
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
@cache.memoize()
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

# average rating callback
df = pd.read_csv("data/processed/processed_cookie_data.csv")

@callback(
    Output("rating_gauge", "figure"),
    Input("rating_gauge", "id"),  # No need for slider input
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value"),
)
@cache.memoize()
def update_gauge_chart(_, rating_range=[0, 1], selected_ingredients=None):
    """
    Compute the average rating and update the gauge with a moving dial color.
    """
    # connect to the ratings slider
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    # If ingredients are selected, filter by those as well
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    # group by recipe ID so that there is only one entry per recipe instead of per ingredient in the recipe
    # the recipe's rating per ingredient should be the same, so "mean" doesn't really do anything
    filtered_df = filtered_df.groupby("Recipe_Index")['Rating'].mean().reset_index()

    # Compute average rating
    avg_rating = filtered_df["Rating"].mean() if not filtered_df.empty else 0

    # Create Plotly Gauge with a dynamically moving dial color
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(avg_rating, 2),
            # title={"text": f"Average Rating: {avg_rating:.2f}", "font": {"size": 16}},
            domain={"x": [0, 1], "y": [0, 1]},   # Fill the entire chart area (full circle)
            gauge={
                "axis": {
                    "range": [0, 1],
                    "tickmode": "linear",
                    "tick0": 0,
                    "dtick": 0.2,
                    "tickfont": {"color": "#000", "size": 12}
                },
                "bar": {"color": "#3E2723", "thickness": 0.3},  # Ensure the dial color is distinct
                "steps": [
                    {"range": [0, avg_rating], "color": "#906A51"},  # Color up to average rating
                    {"range": [avg_rating, 1], "color": "#F5E1C8"},  # Remaining range
                ],
                "threshold": {
                    "line": {"color": "#3E2723", "width": 4},
                    "thickness": 0.75,  # Adjusted for a clear marker
                    "value": avg_rating
                },
                "borderwidth": 0,
                "bordercolor": "#D2A679",
                
            }
        )
    )

    # Adjust layout to fit the small container
    fig.update_layout(
        autosize=True, 
        margin=dict(l=5, r=5, t=35, b=5),
        paper_bgcolor="#D2A679",  # Match outer container
        font=dict(color="#000")
    )

    return fig

# number of recipes per ingredient callbacks
@callback(
    [Output("ingredient_bar_chart", "spec"), Output("remaining-ingredients", "children")], 
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value")
)
@cache.memoize()
def create_ingredient_distribution(rating_range=[0, 1], selected_ingredients=None):
    """
    Generates a bar chart showing the top 10 ingredients and a compact multi-column list of remaining ingredients.
    """
    # Filter data based on rating range
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    # If specific ingredients are selected, filter by those
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]
    
    # Compute the number of unique recipes each ingredient appears in
    df_ingredient_counts = (
        filtered_df.groupby("Ingredient")["Recipe_Index"]
        .nunique()
        .reset_index()
    )
    df_ingredient_counts.columns = ["Ingredient", "Recipe_Count"]

    # Sort ingredients by recipe count
    df_sorted = df_ingredient_counts.sort_values(by="Recipe_Count", ascending=False)

    # Select top 10 ingredients for the bar chart
    df_top_ingredients = df_sorted.head(10)

    # Get the remaining ingredients (those NOT in the top 10)
    df_remaining_ingredients = df_sorted.iloc[10:]

    # Create the bar chart
    chart = (
        alt.Chart(df_top_ingredients)
        .mark_bar()
        .encode(
            alt.X("Recipe_Count:Q",
                  title="Number of Recipes",
                  axis=alt.Axis(gridColor='#D2A679', domainColor="#3E2723", tickColor='#3E2723')),
            alt.Y("Ingredient:N",
                  sort='-x',
                  title="Ingredient",
                  axis=alt.Axis(domainColor="#3E2723", tickColor='#3E2723')),
            tooltip=[alt.Tooltip("Recipe_Count:Q", title="Number of Recipes")],
            color=alt.value('#906A51')
        )
        .properties(
            width="container",
            height=alt.Step(30)  
        )
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelLimit=0,
            labelFontSize=10,
            titleFontSize=12
        ).configure(
        background='#F5E1C8'
        )
    )

    # Create a multi-column inline list
    if not df_remaining_ingredients.empty:
        remaining_content = [
            html.Div(
                f"{row['Ingredient']} ({row['Recipe_Count']})",
                style={"padding": "2px", "whiteSpace": "nowrap"}
            ) 
            for _, row in df_remaining_ingredients.iterrows()
        ]

        remaining_content.insert(0, html.Div("Additional Ingredients:", style={"fontWeight": "bold", "width": "100%"}))
    else:
        remaining_content = html.Div(
            "All ingredients are in the top 10",
            style={"fontStyle": "italic", "width": "100%"}
        )

    return chart.to_dict(), remaining_content

# recipes and complexity callbacks
try:
    df_recipes = pd.read_csv(csv_path)

    # Ensure Complexity_Score exists
    if "Complexity_Score" not in df_recipes.columns:
        df_recipes["Complexity_Score"] = 0  # Default value if missing

    df_recipes["Complexity_Score"] = df_recipes["Complexity_Score"].fillna(0)  # Replace NaN with 0
except FileNotFoundError:
    df_recipes = pd.DataFrame(columns=["Recipe_Index", "Ingredient", "Text", "Rating", "Complexity_Score"])  # Ensure correct columns

@callback(
    [Output("recipe-list", "children"),
     Output("recipe-total", "children")],
    [Input("rating-range", "value"),
     Input("ingredient-checklist", "value")]
)
@cache.memoize()
def update_recipe_list(rating_range=[0, 1], selected_ingredients=None): 
    """
    Updates the displayed list of recipes based on selected ingredients and rating range.
    """
    filtered_df = df_recipes.copy()

    # Filter by rating range
    filtered_df = filtered_df[
        (filtered_df["Rating"] >= rating_range[0]) &
        (filtered_df["Rating"] <= rating_range[1])
    ]

    # Filter by ingredient selection (if ingredients are selected)
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    recipe_count_text = f"Total Recipes: {filtered_df['Recipe_Index'].nunique()}"

    # If no recipes match, show message
    if filtered_df.empty:
        return [html.P("No recipes match the selected criteria.", style={"color": "red", "textAlign": "center"})], recipe_count_text

    # **Group by Recipe_Index and Complexity_Score, concatenate ingredient descriptions**
    grouped_recipes = (
        filtered_df.groupby(["Recipe_Index", "Complexity_Score"])[["Quantity", "Unit", "Ingredient"]]
        .apply(lambda df: "\n".join([f"{round(qty, 1)} {unit} {ing}" for qty, unit, ing in zip(df["Quantity"], df["Unit"], df["Ingredient"])]))
        .reset_index()
        .rename(columns={0: "Formatted_Ingredients"})
    )

    # Display filtered recipes with tooltips for full ingredient descriptions
    recipe_list = []
    for _, row in grouped_recipes.iterrows():
        recipe_id = f"recipe-{row['Recipe_Index']}"  # Unique ID for each list item

        # Create tooltip text with all ingredients
        tooltip_text = f"Ingredients:\n{row['Formatted_Ingredients']}"

        # Create list item with Recipe Index and Complexity Score
        recipe_list.append(
            html.Li(
                f"{row['Recipe_Index']}: {row['Complexity_Score']:.2f}",  # Show Recipe ID + Complexity Score
                id=recipe_id,  # Set ID for tooltip reference
                style={
                    "padding": "5px",
                    "borderBottom": "1px solid #fff",
                    "backgroundColor": "#B88C64",
                    "color": "black",
                    "cursor": "pointer"
                }
            )
        )

        # Add tooltip with **ALL ingredients**
        recipe_list.append(
            dbc.Tooltip(
                tooltip_text,  # Tooltip contains ingredient list
                target=recipe_id,
                placement="right",
                style={"color": "#000", "maxWidth": "300px", "whiteSpace": "pre-wrap"}  # pre-wrap ensures new lines are visible
            )
        )

    return recipe_list, recipe_count_text