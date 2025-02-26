from dash import html

def number_of_recipes_per_ingredient():
    return html.Div(
        "Number of Recipes per Ingredient",
        className="number_of_recipes_per_ingredient",
        style={
            "backgroundColor": "#00008b",
            "color": "#fff",
            "padding": "20px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col9-start",
            "gridRowStart": "row4-start",
            "gridRowEnd": "row9-end"
        }
    )