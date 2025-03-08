import pandas as pd
import altair as alt
from dash import dcc, html, callback, Input, Output
import dash_vega_components as dvc

# Load data
df = pd.read_csv("data/processed/processed_cookie_data.csv")

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
                    style={"width": "100%", "height": "100%"},
                ),
                style={
                    "flex": "0 0 auto",  
                    "borderBottom": "2px solid white",
                    "marginBottom": "10px"
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
                    "fontSize": "0.4em",  
                    "lineHeight": "1.2em",
                    "gap": "5px",
                    "textAlign": "center",
                    "maxHeight": "100%",  
                    "overflow": "hidden"
                }
            )
        ],
        style={
            "backgroundColor": "#D2A679",
            "color": "#fff",
            "padding": "10px",
            "gridColumnStart": "col6-start",
            "gridColumnEnd": "col9-start",
            "gridRowStart": "row4-start",
            "gridRowEnd": "row9-end",
            "display": "flex",
            "flexDirection": "column",
            "height": "100%",
            "boxSizing": "border-box",
            "borderRadius": "5px",
            "border": "2px solid #D2A679",
        }
    )

@callback(
    [Output("ingredient_bar_chart", "spec"), Output("remaining-ingredients", "children")], 
    Input("rating-range", "value"),
    Input("ingredient-checklist", "value")
)
def create_ingredient_distribution(rating_range=[0, 1], selected_ingredients=None):
    """
    Generates a bar chart showing the top 10 ingredients and a compact multi-column list of remaining ingredients.
    """
    # Filter data based on rating range
    filtered_df = df.query('Rating.between(@rating_range[0], @rating_range[1])')

    # If specific ingredients are selected, filter by those
    if selected_ingredients:
        filtered_df = filtered_df[filtered_df["Ingredient"].isin(selected_ingredients)]
    
    # Compute the number of unique recipes each ingredient appears in
    df_ingredient_counts = (
        filtered_df.groupby("Ingredient")["Recipe_Index"]
        .nunique()
        .reset_index()
    )
    df_ingredient_counts.columns = ["Ingredient", "Recipe_Count"]

    # Sort ingredients by recipe count
    df_sorted = df_ingredient_counts.sort_values(by="Recipe_Count", ascending=False)

    # Select top 10 ingredients for the bar chart
    df_top_ingredients = df_sorted.head(10)

    # Get the remaining ingredients (those NOT in the top 10)
    df_remaining_ingredients = df_sorted.iloc[10:]

    # Create the bar chart
    chart = (
        alt.Chart(df_top_ingredients)
        .mark_bar()
        .encode(
            alt.X("Recipe_Count:Q",
                  title="Number of Recipes",
                  axis=alt.Axis(gridColor='#D2A679', domainColor="#3E2723", tickColor='#3E2723')),
            alt.Y("Ingredient:N",
                  sort='-x',
                  title="Ingredient",
                  axis=alt.Axis(domainColor="#3E2723", tickColor='#3E2723')),
            tooltip=[alt.Tooltip("Recipe_Count:Q", title="Number of Recipes")],
            color=alt.value('#906A51')
        )
        .properties(
            width="container",
            height=alt.Step(30)  
        )
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelLimit=0,
            labelFontSize=10,
            titleFontSize=12
        ).configure(
        background='#F5E1C8'
        )
    )

    # Create a multi-column inline list
    if not df_remaining_ingredients.empty:
        remaining_content = [
            html.Div(
                f"{row['Ingredient']} ({row['Recipe_Count']})",
                style={"padding": "2px", "whiteSpace": "nowrap"}
            ) 
            for _, row in df_remaining_ingredients.iterrows()
        ]

        remaining_content.insert(0, html.Div("Additional Ingredients:", style={"fontWeight": "bold", "width": "100%"}))
    else:
        remaining_content = html.Div(
            "All ingredients are in the top 10",
            style={"fontStyle": "italic", "width": "100%"}
        )

    return chart.to_dict(), remaining_content
