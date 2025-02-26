from dash import html

def footer():
    return html.Footer(
        "Footer",
        className="p-2",
        style={
            "backgroundColor": "#f08080",
            "height": "5vh", 
            "margin": "1vh 5vw",
        }
    )