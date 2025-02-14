# Milestone 1 Report
Authors: Mu (Henry) Ha, Javier Martinez, Stephanie Ta, and Zuer (Rebecca) Zhong

## Motivation and Purpose

## Description of the Data

For this project, we have selected the "Choc Chip Cookie Ingredients" dataset, which provides detailed, standardized ingredient information for 211 chocolate chip cookie recipes sourced from various online platforms. The dataset is organized at the ingredient level and comprises roughly 1,200 rows and 6 primary columns.

| Header |  Data Type |Description |
|---|---|---|
| `Ingredient` |string| The standardized name of the ingredient. Variations such as “bleached flour” were consolidated under a single name (e.g., “all purpose flour”).|
| `Text` |string| The complete textual description of the ingredient and its quantity, adjusted to yield 48 cookies per recipe.|
| `Recipe_Index` | string | A unique identifier for each recipe. Prefixes like “AR\_” denote AllRecipes sources, “E\_” denotes Epicurious, and “Misc\_\_” denotes recipes collected by hand. |
| `Rating` | float | A numeric value (0 to 1) representing the recipe’s rating, if available.|
| `Quantity` | float | The amount of the ingredient, scaled to produce 48 cookies. |
| `Unit` | string | The measurement unit for each ingredient.|

This dataset provides a detailed collection of chocolate chip cookie recipes, including standardized ingredient lists and ratings. For individuals with allergies, the standardized ingredient data is particularly valuable as it allows for easy filtering of recipes based on allergen presence. For instance, someone with a nut or gluten allergy can quickly identify and exclude recipes that contain these ingredients, ensuring they select recipes that are safe for them. Additionally, by coupling the ingredient data with recipe ratings, users can filter for not only allergen-free recipes but also those that are highly rated, thereby improving the likelihood of finding the best recipe that meets both safety and quality criteria. 
Moreover, we plan to engineer a new variable, "Ingredient Proportion," which will represent the ratio of each ingredient’s quantity relative to the total ingredient quantity for a given recipe. This variable will help standardize the comparison of ingredients across recipes by highlighting the relative importance of each component within the overall recipe formulation. 
Also, we plan to add two columns to categorize the ingredients for easy filtering. One column with categorical values "basic" vs. "special". "basic" would correspond to ingredients such as flour, sugar, fats, and eggs. "special" would correspond to chocolate and any other ingredient. The other column for ingredient sub-category: "flour", "sugar", "fats", "eggs", "chocolate", and "other"
In addition, we will develop an "Ingredient Popularity Score" for each ingredient, which quantifies how frequently the ingredient appears across the entire dataset; this score will enable us to distinguish between commonly used ingredients and those that are more unique or rare. Finally, we will derive a "Complexity Score" for each recipe. This score will take into account factors such as the number of steps and the structural complexity of the sentences, thereby providing an estimate of how intricate or challenging the recipe might be to execute.

## Research Questions and Usage Scenarios

Emily is a mother of a child with severe food allergies, including an egg allergy, and she wants to find highly rated cookie 
recipes that do not contain eggs. She wants to be able to [explore] the available recipes to [compare] different egg substitutes and [identify] the best-rated alternatives for her child’s diet.

When Emily logs on to our app, she will see an overview of all the available cookie recipes, along with their ratings
and ingredient lists. She can filter out recipes containing eggs and explore alternative ingredients used in highly rated recipes. As she applies the filters, Emily may, for example, notice that "applesauce" and "flaxseed" are commonly used as egg substitutes, and that recipes using flaxseed tend to have higher ratings. This allows her to compare the effectiveness of different substitutes and make an informed decision about which recipes to try.

Based on her findings from using our app, Emily decides to try a highly rated egg-free cookie recipe that uses flaxseed. 
She saves the recipe for future reference and shares it with an allergy-friendly baking group to help others in similar situations.

## App Sketch & Brief Description

The app has a landing page that shows the distribution of cookie recipe ratings as a histogram and the
distribution of the different recipe ingredients as a bar chart.
The number of recipes and average recipe rating will also be displayed.
From the clickable boxes, the user can filter by overall category (basic or special ingredient).
They can filter even further by the ingredient subcategories (Flour, Sugar, Fats, Eggs, Chocolate, and Other) by clicking on the icons.
Additionally, they can filter by specific ingredient from the list of ingredients.
There is also a slider that will allow the user to filter by their desired recipe rating range.

![Dashboard app sketch.](../img/sketch.png)
