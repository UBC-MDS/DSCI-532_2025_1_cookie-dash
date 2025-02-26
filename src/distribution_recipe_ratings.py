from dash import html

def distribution_recipe_ratings():
    return html.Div(
        "Distribution of Recipe Ratings",
        className="distribution_recipe_ratings",
        style={
            "backgroundColor": "#8B0000",
            "color": "#fff",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row6-start",
            "gridRowEnd": "row9-end"
        }
    )