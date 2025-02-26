from dash import html

def header():
    return html.Header(
        "Cookie Dash",
        className="p-2",
        style={
            "backgroundColor": "#add8e6",
            "height": "5vh", 
            "margin": "1vh 5vw",
        }
    )