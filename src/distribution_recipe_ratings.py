import pandas as pd
import altair as alt
from dash import dcc, html, callback, Input, Output
import dash_vega_components as dvc

df = pd.read_csv("data/processed/processed_cookie_data.csv")

def distribution_recipe_ratings():
    return html.Div(
        className="distribution_recipe_ratings",
        children=[
            "Distribution of Recipe Ratings",
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

# Callback to update histogram x-axis based on slider values
@callback(
    Output("rating_histogram", "spec"),
    Input("x-range", "value"),
)
def create_ratings_distribution(x_range=[0, 1]):
    data_in_range = df.query('Rating.between(@x_range[0], @x_range[1])')

    chart = alt.Chart(data_in_range).mark_bar().encode(
        alt.X("Rating:Q", bin=alt.Bin(maxbins=20), title="Rating"),
        alt.Y("count()", title="Count"),
        tooltip=["Rating"]
    ).properties(width=510, height=95)

    return (chart.to_dict())