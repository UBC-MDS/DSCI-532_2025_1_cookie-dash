from dash import html

def average_rating():
    return html.Div(
        "Average Rating",
        className="average_rating",
        style={
            "backgroundColor": "#006400",
            "color": "#fff",
            "padding": "20px",
            "gridColumnStart": "col8-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row4-start"
        }
    )