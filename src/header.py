from dash import html

def header():
    return html.Header(
        html.H1("Cookie Dash 🍪", style={"color": "#ffffff", "paddingLeft": "10px", "margin": "0"}),
        className="p-2",
        style={
            "backgroundColor": "#3E2723",
            "height": "auto", 
            "margin": "1vh 5vw",
            "padding": "20px",
        }
    )