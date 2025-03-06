import pandas as pd
import altair as alt
from dash import dcc, html, callback, Input, Output
import dash_vega_components as dvc

df = pd.read_csv("data/processed/processed_cookie_data.csv")

def distribution_recipe_ratings():
    return html.Div(
        className="distribution_recipe_ratings",
        children=[
            dvc.Vega(id='rating_histogram', spec={}),
            dcc.RangeSlider(
                id='rating-range',
                min=0,
                max=1,
                value=[0, 1],
                step=0.1,
                marks={i: {'label': str(i), 'style': {'color': 'white'}} for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]},
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
        }
    )

# Callback to update histogram x-axis based on slider values
@callback(
    Output("rating_histogram", "spec"),
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value"),
)
def create_ratings_distribution(rating_range=[0, 1], selected_ingredients=None):
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]

    # group by recipe ID so that there is only one entry per recipe instead of per ingredient in the recipe
    # the recipe's rating per ingredient should be the same, so "mean" doesn't really do anything
    filtered_df = filtered_df.groupby("Recipe_Index")['Rating'].mean().reset_index()


    chart = alt.Chart(filtered_df).mark_bar().encode(
        alt.X("Rating:Q", bin=alt.Bin(maxbins=10),
              title="Rating",
              scale=alt.Scale(domain=rating_range),
              axis=alt.Axis(domainColor="#3E2723", tickColor='#3E2723')
              ),
        alt.Y("count():Q",
              title="Count",
              axis=alt.Axis(gridColor='#D2A679', domainColor="#3E2723", tickColor='#3E2723')
              ),
        tooltip=[alt.Tooltip("count():Q", title="Number of Recipes")],
        color=alt.value('#906A51')
    ).properties(title="Distribution of Recipe Ratings", width=535, height=110
    ).configure(background='#F5E1C8').configure_view(strokeWidth=0)

    return (chart.to_dict())