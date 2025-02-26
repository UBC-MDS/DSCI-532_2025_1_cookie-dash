from dash import html

def number_of_recipes():
    return html.Div(
        "Number of Recipes",
        className="number_of_recipes",
        style={
            "backgroundColor": "#90ee90",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col8-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row4-start"
        }
    )