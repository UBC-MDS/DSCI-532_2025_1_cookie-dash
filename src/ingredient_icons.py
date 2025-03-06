from dash import html, callback, Output, Input, ALL, callback_context, State
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
    Build a layout that shows two category blocks side-by-side: basic taking 2/3
    and special taking 1/3 of the available width. Each block has its title on top
    and its subcategory buttons below, all within a flex container.
    """
    categories = ["basic", "special"]
    # Define custom background colors for each category
    category_backgrounds = {
        "basic": "#D2A679",
        "special": "#D2A679"
    }
    
    # Map each subcategory to its corresponding icon URL via the API.
    icon_urls = {
        "flour": "https://api.iconify.design/game-icons:flour.svg",
        "sweetener": "https://api.iconify.design/healthicons:sugar.svg",
        "fat": "https://api.iconify.design/fluent-emoji-high-contrast:butter.svg",
        "egg": "https://api.iconify.design/hugeicons:eggs.svg",
        "other": "https://api.iconify.design/fontisto:test-bottle.svg",
        "chocolate": "https://api.iconify.design/hugeicons:chocolate.svg"
    }
    
    category_blocks = []
    for cat in categories:
        # Hardcode the subcategories for each category
        if cat == "basic":
            subcategories = ["flour", "sweetener", "fat", "egg"]
        elif cat == "special":
            subcategories = ["other", "chocolate"]
        else:
            subcategories = []
        
        # Create subcategory buttons with dynamically set icon URL
        subcat_cards = []
        for subcat in subcategories:
            # Get the URL for the current subcategory. Defaults to the flour icon if not found.
            icon_url = icon_urls.get(subcat, icon_urls["flour"])
            button = dbc.Button(
                children=[
                    html.Img(
                        src=icon_url,
                        style={"width": "50px", "height": "50px"},
                        className="icon"
                    ),
                    # Display the subcategory title below the icon
                    html.Div(
                        subcat, 
                        style={
                            "marginTop": "5px", 
                            "fontWeight": "bold"
                        }
                    )
                ],
                id={"type": "subcategory-button", "index": subcat},
                n_clicks=0,
                color="primary",
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "space-around",
                    "padding": "10px",
                    "marginTop": "15px",
                    "width": "6vw"
                }
            )
            subcat_cards.append(button)
        
        # Each category block: flex container in column direction
        # Basic gets flex: 2 and special gets flex: 1
        category_block = html.Div(
            children=[
                # Category title row
                html.Div(
                    cat.capitalize(),
                    style={
                        "fontWeight": "bold",
                        "fontSize": "24px",
                        "textAlign": "center"
                    }
                ),
                # Subcategory row: flex container in row direction
                html.Div(
                    children=subcat_cards,
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "flexWrap": "wrap",
                        "justifyContent": "space-around",
                        "marginLeft": "3px"
                    }
                )
            ],
            style={
                "flex": "2" if cat == "basic" else "1",
                "backgroundColor": category_backgrounds.get(cat, "#FFFFFF"),
                "padding": "10px",
                "height": "100%",
                "borderRadius": "5px",
                "marginRight": "10px" if cat == "basic" else "0px"
            }
        )
        category_blocks.append(category_block)
    
    # Outer container: still using grid CSS properties and flex box for internal layout
    return html.Div(
        children=category_blocks,
        style={
            "backgroundColor": "#744F44",
            "color": "#000",
            "padding": "20px",
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "space-around",
            "alignItems": "flex-start",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row3-start",
            "overflowY": "auto",
            "borderRadius": "5px",
            "border": "2px solid #744F44",
        },
        className="ingredient_icons"
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