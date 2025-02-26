from dash import html

def ingredient_icons():
    return html.Div(
        "Ingredient Icons",
        className="ingredient_icons",
        style={
            "backgroundColor": "#696969",
            "color": "#fff",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row3-start"
        }
    )