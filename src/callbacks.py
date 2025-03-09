from dash import callback, Output, Input, State, callback_context, ALL
import pandas as pd
import ast

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