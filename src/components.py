from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

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
                   style={"font-size": "12px", "margin-bottom": "2px", "margin-top": "0px"}),

            html.P([
                "Developers: Mu (Henry) Ha, Javier Martinez, Stephanie Ta, and Zuer (Rebecca) Zhong.",
                html.Span("  ", style={"white-space": "pre"}),
                "Last updated: March 15, 2025",
                html.Span("  ", style={"white-space": "pre"}),
                html.A("GitHub Repository", href="https://github.com/UBC-MDS/DSCI-532_2025_1_cookie-dash",
                       style={"font-size": "12px", "lineHeight": "1"})
            ], style={"font-size": "12px", "margin-bottom": "2px"}),
        ],
        className="p-2",
        style={
            "height": "auto",
            "margin": "1vh 5vw",
        }
    )

def ingredient_icons():
    """
    Build a layout that shows two category blocks side-by-side: basic taking 2/3
    and special taking 1/3 of the available width. Each block has its title on top
    and its subcategory buttons below, all within a flex container.
    """
    categories = ["basic", "special"]
    # Define custom background colors for each category
    category_backgrounds = {
        "basic": "#D2A679",
        "special": "#D2A679"
    }
    
    # Map each subcategory to its corresponding icon URL via the API.
    icon_urls = {
        "flour": "https://api.iconify.design/game-icons:flour.svg",
        "sweetener": "https://api.iconify.design/healthicons:sugar.svg",
        "fat": "https://api.iconify.design/fluent-emoji-high-contrast:butter.svg",
        "egg": "https://api.iconify.design/hugeicons:eggs.svg",
        "other": "https://api.iconify.design/fontisto:test-bottle.svg",
        "chocolate": "https://api.iconify.design/hugeicons:chocolate.svg"
    }
    
    category_blocks = []
    for cat in categories:
        # Hardcode the subcategories for each category
        if cat == "basic":
            subcategories = ["flour", "sweetener", "fat", "egg"]
        elif cat == "special":
            subcategories = ["other", "chocolate"]
        else:
            subcategories = []
        
        # Create subcategory buttons with dynamically set icon URL
        subcat_cards = []
        for subcat in subcategories:
            # Get the URL for the current subcategory. Defaults to the flour icon if not found.
            icon_url = icon_urls.get(subcat, icon_urls["flour"])
            button = dbc.Button(
                children=[
                    html.Img(
                        src=icon_url,
                        style={"width": "50px", "height": "50px"},
                        className="icon"
                    ),
                    # Display the subcategory title below the icon
                    html.Div(
                        subcat, 
                        style={
                            "marginTop": "5px", 
                            "fontWeight": "bold"
                        }
                    )
                ],
                id={"type": "subcategory-button", "index": subcat},
                n_clicks=0,
                color="primary",
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "space-around",
                    "padding": "10px",
                    "marginTop": "15px",
                    "width": "6vw"
                }
            )
            subcat_cards.append(button)
        
        # Each category block: flex container in column direction
        # Basic gets flex: 2 and special gets flex: 1
        category_block = html.Div(
            children=[
                # Category title row
                html.H6(
                    cat.capitalize(),
                    style={
                        "textAlign": "center"
                    }
                ),
                # Subcategory row: flex container in row direction
                html.Div(
                    children=subcat_cards,
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "flexWrap": "wrap",
                        "justifyContent": "space-around",
                        "marginLeft": "3px"
                    }
                )
            ],
            style={
                "flex": "2" if cat == "basic" else "1",
                "backgroundColor": category_backgrounds.get(cat, "#FFFFFF"),
                "padding": "10px",
                "height": "100%",
                "borderRadius": "5px",
                "marginRight": "10px" if cat == "basic" else "0px"
            }
        )
        category_blocks.append(category_block)
    
    # Outer container: still using grid CSS properties and flex box for internal layout
    return html.Div(
        children=category_blocks,
        style={
            "backgroundColor": "#744F44",
            "color": "#000",
            "padding": "5px",
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "space-around",
            "alignItems": "flex-start",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row3-start",
            "overflowY": "auto",
            "borderRadius": "5px",
            "border": "2px solid #744F44",
        },
        className="ingredient_icons"
    )

def ingredient_filter():
    return html.Div(
        id="ingredient-filter-div",
        style={
            "backgroundColor": "#906A51",
            "color": "#000",
            "padding": "20px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row3-start",
            "gridRowEnd": "row6-start",
            "borderRadius": "5px",
            "overflowY": "auto",
            "border": "2px solid #906A51",
        },
        children=[
            html.Div(
                style={"width": "100%", "display": "flex"},
                children=[
                    # Left side: Available Ingredients title with header row and checklist
                    html.Div(
                        style={"width": "66%", "paddingRight": "10px"},
                        children=[
                            html.Div(
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center"
                                },
                                children=[
                                    html.H4("Available Ingredients", style={"margin": 0}),
                                    dbc.Button(
                                        "Deselect All",
                                        id="deselect-all-button",
                                        n_clicks=0,
                                        style={"marginLeft": "10px"}
                                    )
                                ]
                            ),
                            # Header row for columns
                            html.Div(
                                children=[
                                    html.Span("Ingredient", style={"flex": "1", "textAlign": "left"}),
                                    html.Span("Popularity Score", style={"minWidth": "50px", "textAlign": "right"})
                                ],
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center",
                                    "fontWeight": "bold",
                                    "padding": "4px 8px",
                                    "borderBottom": "1px solid #ccc",
                                    "marginTop": "10px"
                                }
                            ),
                            # Checklist with custom label styling so checkbox and label share the same row.
                            dcc.Checklist(
                                id="ingredient-checklist",
                                options=[],  # options are generated in the callback below
                                value=[],    # initially no ingredient is selected
                                labelStyle={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center",
                                    "width": "100%",
                                    "padding": "4px 8px"
                                },
                                style={"display": "block", "marginTop": "5px"}
                            )
                        ]
                    ),
                    # Right side: Selected Ingredients (only names)
                    html.Div(
                        style={"width": "34%", "paddingLeft": "10px", "borderLeft": "1px solid #aaa"},
                        children=[
                            html.H4("Selected Ingredients"),
                            html.Ul(id="selected-ingredients-list", children=[])
                        ]
                    )
                ]
            )
        ]
    )

def distribution_recipe_ratings():
    return html.Div(
        className="distribution_recipe_ratings",
        children=[
            html.H6("Distribution of Recipe Ratings", style={'color':'black', "textAlign": "center"}),
            dvc.Vega(id='rating_histogram',
                     spec={},
                     style={"width": "100%", "height": "70%"}),
            dcc.RangeSlider(
                id='rating-range',
                min=0,
                max=1,
                value=[0, 1],
                step=0.1,
                marks={i: {'label': str(i), 'style': {'color': 'black'}} for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]},
                className="rating-slider",
            )
        ],
        style={
            "backgroundColor": "#D2A679",
            "color": "#fff",
            "padding": "10px",
            "gridColumnStart": "col1-start",
            "gridColumnEnd": "col6-start",
            "gridRowStart": "row6-start",
            "gridRowEnd": "row9-end",
            "borderRadius": "5px",
            "border": "2px solid #D2A679",
            # "justifyContent": "center",  # Centers horizontally
            # "alignItems": "center",  # Centers vertically
        }
    )

def average_rating():
    """
    Display a Plotly Gauge inside a small-sized container.
    """
    return html.Div(
        className="average_rating",
        children=[
            html.H6("Average Rating:", style={'color':'black', "textAlign": "center"}),
            dcc.Graph(
                id="rating_gauge",
                config={"displayModeBar": False},  # Hide toolbar
                style={
                    "width": "80%",   # Dynamic chart width
                    "height": "75%"   # Dynamic chart height
                }
            )
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            # "justifyContent": "center",
            "alignItems": "center",
            "justifyContent": "flex-start",
            "backgroundColor": "#D2A679",
            "color": "#fff",
            "padding": "15px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col9-start",
            "gridRowStart": "row6-start",
            "gridRowEnd": "row9-end",
            "overflow": "hidden",  # Clip slight overflow
            "borderRadius": "5px",
            "border": "2px solid #D2A679",
        }
    )

def number_of_recipes_per_ingredient():
    """
    Returns a container with a fully visible bar chart and a compact multi-column list of remaining ingredients.
    """
    return html.Div(
        className="number_of_recipes_per_ingredient",
        children=[
            # Title
            html.H6("Top 10 Ingredients by Number of Recipes", style={'color':'black', "textAlign": "center"}),

            # Responsive Bar Chart
            html.Div(
                dvc.Vega(
                    id='ingredient_bar_chart',
                    spec={},
                    style={"width": "100%", "height": "35%"},  
                ),
                style={
                    "flex": "0 0 auto",  
                    "borderBottom": "2px solid white",
                    "marginBottom": "2px"
                }
            ),
            
            # Multi-column Compact Remaining Ingredients List 
            html.Div(
                id="remaining-ingredients",
                style={
                    "flex": "1",  
                    "padding": "5px",
                    "backgroundColor": "#F5E1C8",
                    "borderRadius": "5px",
                    "color": "#000",
                    "display": "flex",
                    "flexWrap": "wrap",  
                    "justifyContent": "center",
                    "alignItems": "center",
                    "fontSize": "0.7em",  
                    "lineHeight": "1.5em",
                    "gap": "5px",
                    "textAlign": "center",
                    "maxHeight": "150px",  
                    "overflowY": "auto"  
                }
            )
        ],
        style={
            "backgroundColor": "#D2A679",
            "color": "#fff",
            "padding": "10px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col9-start",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row6-start",
            "display": "flex",
            "flexDirection": "column",
            "height": "100%",
            "boxSizing": "border-box",
            "borderRadius": "5px",
            "border": "2px solid #D2A679",
        }
    )



def recipes_and_complexity():
    """
    Returns a styled container displaying a dynamically filtered recipe list.
    """
    return html.Div(
        [
            html.H6("Recipes & Complexity", style={'color':'black', "textAlign": "center"}),

            # Display count of recipes
            html.P(id="recipe-total", children="Total Recipes: 0",
                   style={"textAlign": "center", "color": "#000", "marginBottom": "10px"}),

            # Container for recipe list
            html.Ul(
                id="recipe-list", style={
                "listStyleType": "none",
                "padding": "10px",
                "height": "80%",
                "overflowY": "auto",
                "backgroundColor": "#F5E1C8",
                "textAlign": "left",
                "fontSize": "14px"
            }),
        ],
        className="recipes_and_complexity",
        style={
            "backgroundColor": "#B88C64",
            "color": "#000",
            "padding": "10px",
            "borderRadius": "5px",
            "border": "2px solid #B88C64",
            "gridColumnStart": "col9-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row9-end"
        }
    )