from dash import dcc, html, callback
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv("data/processed/processed_cookie_data.csv")

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
            "padding": "10px",
            "gridColumnStart": "col8-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row4-start",
            "overflow": "hidden",  # Clip slight overflow
            "borderRadius": "5px",
            "border": "2px solid #D2A679",
        }
    )

@callback(
    Output("rating_gauge", "figure"),
    Input("rating_gauge", "id"),  # No need for slider input
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value"),
)
def update_gauge_chart(_, rating_range=[0, 1], selected_ingredients=None):
    """
    Compute the average rating and update the gauge with a moving dial color.
    """
    # connect to the ratings slider
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    # If ingredients are selected, filter by those as well
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    # group by recipe ID so that there is only one entry per recipe instead of per ingredient in the recipe
    # the recipe's rating per ingredient should be the same, so "mean" doesn't really do anything
    filtered_df = filtered_df.groupby("Recipe_Index")['Rating'].mean().reset_index()

    # Compute average rating
    avg_rating = filtered_df["Rating"].mean() if not filtered_df.empty else 0

    # Create Plotly Gauge with a dynamically moving dial color
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(avg_rating, 2),
            # title={"text": f"Average Rating: {avg_rating:.2f}", "font": {"size": 16}},
            domain={"x": [0, 1], "y": [0, 1]},   # Fill the entire chart area (full circle)
            gauge={
                "axis": {
                    "range": [0, 1],
                    "tickmode": "linear",
                    "tick0": 0,
                    "dtick": 0.2,
                    "tickfont": {"color": "#000", "size": 12}
                },
                "bar": {"color": "#3E2723", "thickness": 0.3},  # Ensure the dial color is distinct
                "steps": [
                    {"range": [0, avg_rating], "color": "#906A51"},  # Color up to average rating
                    {"range": [avg_rating, 1], "color": "#F5E1C8"},  # Remaining range
                ],
                "threshold": {
                    "line": {"color": "#3E2723", "width": 4},
                    "thickness": 0.75,  # Adjusted for a clear marker
                    "value": avg_rating
                },
                "borderwidth": 0,
                "bordercolor": "#D2A679",
                
            }
        )
    )

    # Adjust layout to fit the small container
    fig.update_layout(
        autosize=True, 
        margin=dict(l=5, r=5, t=35, b=5),
        paper_bgcolor="#D2A679",  # Match outer container
        font=dict(color="#000")
    )

    return fig

def number_of_recipes_per_ingredient():
    """
    Display a horizontal bar chart showing the number of recipes per ingredient.
    """
    return html.Div(
        className="number_of_recipes_per_ingredient",
        children=[
            dcc.Graph(
                id='ingredient_bar_chart',
                config={"displayModeBar": False},
                style={"width": "100%", "height": "250px"}
            )
        ],
        style={
            "backgroundColor": "#00008b",
            "color": "#fff",
            "padding": "20px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col9-start",
            "gridRowStart": "row4-start",
            "gridRowEnd": "row9-end",
        }
    )

@callback(
    Output("ingredient_bar_chart", "figure"),
    Input("ingredient_bar_chart", "id")  # No need for interactive filtering
)
def update_ingredient_chart(_):
    """
    Generate a horizontal bar chart displaying ingredient distribution.
    """
    ingredient_counts = df["Ingredient"].value_counts().reset_index()
    ingredient_counts.columns = ["Ingredient", "Count"]
    
    fig = go.Figure(
        go.Bar(
            y=ingredient_counts["Ingredient"],
            x=ingredient_counts["Count"],
            orientation='h',
            marker=dict(color='white', line=dict(color='black', width=2))
        )
    )
    
    fig.update_layout(
        title={"text": "Number of Recipes per Ingredient", "font": {"size": 16}, "x": 0.5, "y": 0.95, "xanchor": "center", "yanchor": "top", "bgcolor": "lightgray"},
        xaxis_title="Number of Recipes",
        yaxis_title="",
        plot_bgcolor="#00008b",
        paper_bgcolor="#00008b",
        font=dict(color="white"),
        xaxis=dict(showgrid=False, zeroline=True, zerolinecolor="white", zerolinewidth=2, tickcolor="white"),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=50, r=20, t=50, b=40)
    )
    return fig

