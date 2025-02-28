from dash import html, callback, Output, Input
import pandas as pd

# Load processed data
csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    df_recipes = pd.DataFrame(columns=["Recipe_Index", "Complexity_Score", "Rating", "Ingredient"])  # Empty DataFrame if missing


def recipes_and_complexity():
    """
    Returns a styled container displaying a dynamically filtered recipe list.
    """
    return html.Div(
        [
            html.H4("Recipes & Complexity", style={"textDecoration": "underline", "textAlign": "center"}),

            # Container for recipe list
            html.Ul(id="recipe-list", style={
                "listStyleType": "none",
                "padding": "10px",
                "maxHeight": "250px",
                "overflowY": "auto",
                "border": "1px solid #000",
                "borderRadius": "5px",
                "backgroundColor": "#fff",
                "textAlign": "left",
                "fontSize": "14px"
            }),
        ],
        className="recipes_and_complexity",
        style={
            "backgroundColor": "#32cd32",
            "color": "#000",
            "padding": "20px",
            "borderRadius": "5px",
            "border": "2px solid #228B22",
            "boxShadow": "3px 3px 5px rgba(0, 0, 0, 0.3)",
            "gridColumnStart": "col9-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row4-start",
            "gridRowEnd": "row9-end"
        }
    )


@callback(
    Output("recipe-list", "children"),
    Input("ingredient-select", "value"),
    Input("rating-slider", "value")
)
def update_recipe_list(selected_ingredients, selected_rating_range):
    """
    Updates the displayed list of recipes based on selected ingredients and rating range.

    Parameters:
    -----------
    selected_ingredients : list
        List of selected ingredients from the dropdown.
    selected_rating_range : list
        A list containing the min and max rating scores selected.

    Returns:
    --------
    list of html.Li elements displaying filtered recipes.
    """
    filtered_df = df_recipes.copy()

    # Filter by rating range
    filtered_df = filtered_df[
        (filtered_df["Rating"] >= selected_rating_range[0]) &
        (filtered_df["Rating"] <= selected_rating_range[1])
    ]

    # Filter by ingredient selection (if ingredients are selected)
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    # If no recipes match, show message
    if filtered_df.empty:
        return [html.P("No recipes match the selected criteria.", style={"color": "red", "textAlign": "center"})]

    # Display filtered recipes with complexity scores
    return [
        html.Li(
            f"{row['Recipe_Index']}: {row['Complexity_Score']}",
            style={"padding": "5px", "borderBottom": "1px solid #ccc"}
        )
        for _, row in filtered_df.iterrows()
    ]
