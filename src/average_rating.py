from dash import dcc, html, callback
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv("data/processed/processed_cookie_data.csv")

def average_rating():
    """
    Display a Plotly Gauge inside a small-sized green background container.
    """
    return html.Div(
        className="average_rating",
        children=[
            dcc.Graph(
                id="rating_gauge",
                config={"displayModeBar": False},  # Hide toolbar
                style={
                    "width": "220px",   # Fixed chart width
                    "height": "180px"   # Fixed chart height
                }
            )
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "flex-start",
            "backgroundColor": "#006400",
            "color": "#fff",
            "padding": "10px",
            "gridColumnStart": "col8-start",
            "gridColumnEnd": "col11-end",
            "gridRowStart": "row1-start",
            "gridRowEnd": "row4-start",
            "overflow": "hidden"  # Clip slight overflow
        }
    )

@callback(
    Output("rating_gauge", "figure"),
    Input("rating_gauge", "id"),  # No need for slider input
    Input("rating-range", "value"),
)
def update_gauge_chart(_):
    """
    Compute the average rating and update the gauge with a moving dial color.
    """
    # connect to the ratings slider
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    # group by recipe ID so that there is only one entry per recipe instead of per ingredient in the recipe
    # the recipe's rating per ingredient should be the same, so "mean" doesn't really do anything
    filtered_df = filtered_df.groupby("Recipe_Index")['Rating'].mean().reset_index()

    # Compute average rating
    avg_rating = filtered_df["Rating"].mean() if not filtered_df.empty else 0

    # Create Plotly Gauge with a dynamically moving dial color
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_rating,
            title={"text": f"Average Rating: {avg_rating:.2f}", "font": {"size": 16, "color": "#fff"}},
            domain={"x": [0, 1], "y": [0, 1]},   # Fill the entire chart area (full circle)
            gauge={
                "axis": {
                    "range": [0, 10],
                    "tickmode": "linear",
                    "tick0": 0,
                    "dtick": 2,
                    "tickfont": {"color": "#fff", "size": 12}
                },
                "bar": {"color": "red", "thickness": 0.3},  # Ensure the dial color is distinct
                "steps": [
                    {"range": [0, avg_rating], "color": "lightblue"},  # Color up to average rating
                    {"range": [avg_rating, 10], "color": "lightgray"},  # Remaining range
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,  # Adjusted for a clear marker
                    "value": avg_rating
                },
                "borderwidth": 0,
                "bordercolor": "#006400"
            }
        )
    )

    # Adjust layout to fit the small container
    fig.update_layout(
        autosize=False,
        width=220,      # Same as dcc.Graph style
        height=180,     # Same as dcc.Graph style
        margin=dict(l=5, r=5, t=35, b=5),
        paper_bgcolor="#006400",  # Match outer container
        font=dict(color="#fff")
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
            "gridRowEnd": "row9-end"
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

