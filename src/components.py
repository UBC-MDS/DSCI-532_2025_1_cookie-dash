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
            "borderRadius": "5px",
            "border": "2px solid #3E2723",
        }
    )

def footer():
    return html.Footer(
        children=[
            html.P("Cookie Dash interactive dashboard empowers home bakers and culinary enthusiasts to filter and compare chocolate chip cookie recipes based on ingredient types, ratings, and complexity using dynamic visualizations.",
                    style={"font-size": "12px", "margin-bottom": "2px"}),
            html.P("Developers: Mu (Henry) Ha, Javier Martinez, Stephanie Ta, and Zuer (Rebecca) Zhong. Last updated: March 1, 2025",
                       style={"font-size": "12px", "margin-bottom": "2px"}),
            html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2025_1_cookie-dash",
                       target="_blank", style={"font-size": "12px", "lineHeight": "1"}),
            ],
        className="p-2",
        style={
            "height": "auto", 
            "margin": "1vh 5vw",
        }
    )