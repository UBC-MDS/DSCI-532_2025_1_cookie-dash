from dash import html, callback, Output, Input, ALL, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import ast

csv_path = "data/processed/processed_cookie_data.csv"

try:
    df_recipes = pd.read_csv(csv_path)
except FileNotFoundError:
    # Create empty DataFrame with expected columns if CSV not found
    df_recipes = pd.DataFrame(
        columns=["Recipe_Index", "Complexity_Score", "Rating", "Ingredient", "category", "subcategory"]
    )

def ingredient_icons():
    """
    Build a layout that shows a Title (Category) and, below it,
    a row of clickable subcategory cards for that category.
    """
    # Get all unique categories
    categories = df_recipes["category"].dropna().unique()
    all_components = []
    for cat in categories:
        # Filter the DataFrame for this category, gather subcategories
        df_cat = df_recipes[df_recipes["category"] == cat]
        subcategories = df_cat["subcategory"].dropna().unique()
        # Create a row of cards for each subcategory
        subcat_cards = []
        for subcat in subcategories:
            card = dbc.Card(
                dbc.CardBody(
                    dbc.Button(
                        subcat,
                        id={"type": "subcategory-button", "index": subcat},  # pattern-matching ID
                        n_clicks=0,
                        style={"width": "100%"}
                    )
                ),
                style={"margin": "5px", "width": "150px"}
            )
            subcat_cards.append(card)
        # Add the Category title (H3) and the row of subcategory cards
        all_components.append(html.H3(cat, style={"marginTop": "15px"}))
        all_components.append(
            dbc.Row(subcat_cards, className="g-0", style={"flexWrap": "wrap"})
        )

    return html.Div(
        children=all_components,
        className="ingredient_icons",
        style={
            "backgroundColor": "#696969",
            "color": "#fff",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row3-start",
            "overflowY": "auto"
        }
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