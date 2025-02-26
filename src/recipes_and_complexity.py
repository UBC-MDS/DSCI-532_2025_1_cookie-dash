from dash import html

def recipes_and_complexity():
    return html.Div(
        "Recipes & Complexity",
        className="recipes_and_complexity",
        style={
            "backgroundColor": "#32cd32",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col9-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row4-start",
            "gridRowEnd": "row9-end"
        }
    )