from dash import html

def footer():
    return html.Footer(
        children=[
            html.P("Cookie Dash interactive dashboard empowers home bakers and culinary enthusiasts to filter and compare chocolate chip cookie recipes based on ingredient types, ratings, and complexity using dynamic visualizations.",
                    style={"font-size": "12px"}),
            html.P("Developers: Mu (Henry) Ha, Javier Martinez, Stephanie Ta, and Zuer (Rebecca) Zhong.",
                       style={"font-size": "12px"}),
            html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2025_1_cookie-dash",
                       target="_blank", style={"font-size": "12px"}),
            html.P("Last updated: March 1, 2025",
                       style={"font-size": "12px"}),
            ],
        className="p-2",
        style={
            "backgroundColor": "#fff",
            "height": "5vh", 
            "margin": "1vh 5vw",
        }
    )