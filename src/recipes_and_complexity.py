from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc  # For tooltip support
import pandas as pd

# Load processed data
csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)

    # Ensure Complexity_Score exists
    if "Complexity_Score" not in df_recipes.columns:
        df_recipes["Complexity_Score"] = 0  # Default value if missing

    df_recipes["Complexity_Score"] = df_recipes["Complexity_Score"].fillna(0)  # Replace NaN with 0
except FileNotFoundError:
    df_recipes = pd.DataFrame(columns=["Recipe_Index", "Ingredient", "Text", "Rating", "Complexity_Score"])  # Ensure correct columns


def recipes_and_complexity():
    """
    Returns a styled container displaying a dynamically filtered recipe list.
    """
    return html.Div(
        [
            html.H6("Recipes & Complexity", style={'color':'black', "textAlign": "center"}),

            # Display count of recipes
            html.P(id="recipe-total", children="Total Recipes: 0",
                   style={"textAlign": "center", "color": "#000", "marginBottom": "10px"}),

            # Container for recipe list
            html.Ul(
                id="recipe-list", style={
                "listStyleType": "none",
                "padding": "10px",
                #"maxHeight": "320px",
                "height": "80%", # make height dynamic
                "overflowY": "auto",
                "backgroundColor": "#F5E1C8",
                "textAlign": "left",
                "fontSize": "14px"
            }),
        ],
        className="recipes_and_complexity",
        style={
            "backgroundColor": "#B88C64",
            "color": "#000",
            "padding": "10px",
            "borderRadius": "5px",
            "border": "2px solid #B88C64",
            "gridColumnStart": "col9-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row4-start",
            "gridRowEnd": "row9-end"
        }
    )


@callback(
    [Output("recipe-list", "children"),
     Output("recipe-total", "children")],
    [Input("rating-range", "value"),
     Input("ingredient-checklist", "value")]
)
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
