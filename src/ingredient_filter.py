from dash import html

def ingredient_filter():
    return html.Div(
        "Ingredient Filter",
        className="ingredient_filter",
        style={
            "backgroundColor": "#d3d3d3",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row3-start",
            "gridRowEnd": "row6-start"
        }
    )