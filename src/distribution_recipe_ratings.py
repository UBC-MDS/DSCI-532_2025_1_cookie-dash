import pandas as pd
import altair as alt
from dash import dcc, html, callback, Input, Output
import dash_vega_components as dvc
# import dash_vtk  # Ensure Dash can render Altair charts

df = pd.read_csv("data/processed/processed_cookie_data.csv")

def distribution_recipe_ratings():
    return html.Div(
        className="distribution_recipe_ratings",
        children=[
            html.H4("Distribution of Recipe Ratings", style={"color": "white", "textAlign": "center"}),
            dvc.Vega(id='rating_histogram', spec={}),
            dcc.RangeSlider(
                id='x-range',
                min=df['Rating'].min(),
                max=df['Rating'].max(),
                value=[df['Rating'].min(), df['Rating'].max()],
            )
        ],
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



# Callback to update histogram based on slider values
@callback(
    Output("rating_histogram", "figure"),
    Input("x-range", "value"),
)
def create_ratings_distribution(x_range=[0, 10]):
    # Altair histogram with dynamic x-axis limits
    chart = alt.Chart(df).mark_bar().encode(
        alt.X("Rating:Q", bin=alt.Bin(maxbins=20), title="Rating", scale=alt.Scale(domain=[x_range[0], x_range[1]])),
        alt.Y("count()", title="Count"),
        tooltip=["Rating"]
    ).properties(title="Distribution of Recipe Ratings", width=600)

    return chart.interactive().to_dict()