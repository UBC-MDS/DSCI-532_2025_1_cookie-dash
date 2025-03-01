import pandas as pd
import altair as alt
from dash import dcc, html, callback, Input, Output
import dash_vega_components as dvc

# Load data
df = pd.read_csv("data/processed/processed_cookie_data.csv")

def number_of_recipes_per_ingredient():
  """
  Returns a blue container (grid area) with a bar chart (without a slider).
  """
  return html.Div(
      className="number_of_recipes_per_ingredient",
      children=[
          # Vega component for the bar chart
          dvc.Vega(
              id='ingredient_bar_chart',
              spec={},
              # Let the chart fill the container’s width/height, show scroll if needed
              style={"width": "100%", "height": "100%"}
          ),
      ],
      style={
          "backgroundColor": "#00008b",
          "color": "#fff",
          "padding": "10px",
          # Place this in the grid area you want:
          "gridColumnStart": "col6-start",
          "gridColumnEnd": "col9-start",
          "gridRowStart": "row4-start",
          "gridRowEnd": "row9-end",
          # If chart is still bigger than the box, show scroll
          "overflow": "auto"
      }
  )

@callback(
   Output("ingredient_bar_chart", "spec"), 
   Input("ingredient_bar_chart", "id"),
   Input("rating-range", "value"),
)
def create_ingredient_distribution(_, rating_range=[0, 1]):
   """
   Generates an Altair bar chart showing the number of recipes per ingredient.
   """
   # connect to the ratings slider
   filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')
   
   # Compute how many distinct recipes each ingredient appears in
   df_ingredient_counts = filtered_df.groupby("Ingredient")["Recipe_Index"].nunique().reset_index()
   df_ingredient_counts.columns = ["Ingredient", "Recipe_Count"]

   chart = (
       alt.Chart(df_ingredient_counts)
       .mark_bar()
       .encode(
           alt.X("Recipe_Count:Q", title="Number of Recipes"),
           alt.Y("Ingredient:N", sort='-x', title="Ingredient"),
           tooltip=[alt.Tooltip("Recipe_Count:Q", title="Number of Recipes")]
       )
       .properties(
           title="Number of Recipes per Ingredient",
           width=140,
           height=450
       )
   )


   return chart.to_dict()


