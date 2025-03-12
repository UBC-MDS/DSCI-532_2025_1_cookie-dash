# data_reading_and_processing.py
# authors: Mu (Henry) Ha, Javier Martinez, Stephanie Ta
# date: 2025-02-25

# This script reads in the raw data from the web and saves it to data/raw/raw_cookie_data.csv.
# Then, it proccesses the raw data by generating the missing rating values.
# It also engineers new features: ingredient category, ingredient subcategory, 
# ingredient proportion, ingredient popularity score, and complexity score.
# Also saves the processed data to data/processed/processed_cookie_data.csv.

# Usage from the project root:
# python src/data_reading_and_processing.py

import pandas as pd
import requests
import io

def read_data() -> pd.DataFrame:
    """
    Reads data from a predefined URL into a Pandas DataFrame.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing the data from the specified URL.

    Raises:
    -------
    ValueError:
        If the data cannot be retrieved or parsed.

    Example:
    --------
    >>> df = read_data()
    >>> print(df.head())
    """
    url = "https://raw.githubusercontent.com/the-pudding/data/master/cookies/choc_chip_cookie_ingredients.csv"

    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text), index_col=0)        
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def sub_categorize_ingredient(ingredient, flour_types, sweetener_types, fat_types, chocolate_types):
    """
    Categorizes an ingredient into a specific subcategory based on predefined ingredient types.

    Parameters
    ----------
    ingredient : str
        The ingredient to categorize.
    flour_types : list of str
        A list of ingredients considered as flour.
    sweetener_types : list of str
        A list of ingredients considered as sweeteners.
    fat_types : list of str
        A list of ingredients considered as fats.
    chocolate_types : list of str
        A list of ingredients considered as chocolate.

    Returns
    -------
    str
        The category of the ingredient. Possible values:
        - "flour" if the ingredient is in `flour_types`
        - "sweetener" if the ingredient is in `sweetener_types`
        - "fat" if the ingredient is in `fat_types`
        - "egg" if the ingredient is "egg"
        - "chocolate" if the ingredient is in `chocolate_types`
        - "other" if the ingredient does not match any category

    Examples
    --------
    >>> flour_list = ["all purpose flour", "whole wheat flour"]
    >>> sweetener_list = ["sugar", "honey"]
    >>> fat_list = ["butter", "oil"]
    >>> chocolate_list = ["cocoa powder", "chocolate chips"]
    
    >>> sub_categorize_ingredient("all purpose flour", flour_list, sweetener_list, fat_list, chocolate_list)
    'flour'
    
    >>> sub_categorize_ingredient("honey", flour_list, sweetener_list, fat_list, chocolate_list)
    'sweetener'
    
    >>> sub_categorize_ingredient("egg", flour_list, sweetener_list, fat_list, chocolate_list)
    'egg'
    
    >>> sub_categorize_ingredient("cocoa powder", flour_list, sweetener_list, fat_list, chocolate_list)
    'chocolate'
    
    >>> sub_categorize_ingredient("vanilla extract", flour_list, sweetener_list, fat_list, chocolate_list)
    'other'
    """
    if ingredient in flour_types:
        return "flour"
    elif ingredient in sweetener_types:
        return "sweetener"
    elif ingredient in fat_types:
        return "fat"
    elif ingredient == "egg":
        return "egg"
    elif ingredient in chocolate_types:
        return "chocolate"
    else:
        return "other"

def categorize_subcategory(subcategory):
    """
    Categorizes an ingredient subcategory as either 'basic' or 'special'.

    Parameters
    ----------
    subcategory : str
        The subcategory of the ingredient (e.g., "flour", "sweetener", "chocolate").

    Returns
    -------
    str
        - "basic" if the subcategory is in ["flour", "sweetener", "fat", "egg"].
        - "special" if the subcategory is in ["chocolate", "other"].
        - None if the subcategory does not match any known category.

    Examples
    --------
    >>> categorize_subcategory("flour")
    'basic'

    >>> categorize_subcategory("chocolate")
    'special'

    >>> categorize_subcategory("spice")
    None
    """
    basic_categories = ["flour", "sweetener", "fat", "egg"]
    special_categories = ["chocolate", "other"]
    if subcategory in basic_categories:
        return "basic"
    elif subcategory in special_categories:
        return "special"

def engineer_categories_and_subcategories(raw_data):
    """
    Engineers the features: ingredient category and subcategory.
    Returns a pandas dataframe with the new features.
    """
    # get array of unique ingredients in raw_data
    unique_ingredients = raw_data["Ingredient"].unique()

    # get list of flour types in raw_data
    flour_types = []
    for i in unique_ingredients:
        if "flour" in i:
            flour_types.append(i)

    # get list of sugar types in raw_data
    sugar_types = []
    for i in unique_ingredients:
        if "sugar" in i:
            sugar_types.append(i)
    
    # define a list of sweetener types
    sweetener_types = sugar_types + ["corn syrup", "honey", "molasses", "applesauce"]

    # define a list of fat_types
    fat_types = ["butter", "margarine", "shortening", "vegetable oil"]

    # get list of chocolate types in raw_data
    chocolate_types = []
    for i in unique_ingredients:
        if "chocolate" in i:
            chocolate_types.append(i)
    
    data_with_categories_and_subcategories = raw_data.copy()

    # create subcategory column
    data_with_categories_and_subcategories["subcategory"] = data_with_categories_and_subcategories["Ingredient"].apply(
        sub_categorize_ingredient,
        args=(flour_types, sweetener_types, fat_types, chocolate_types)
        )

    # create category column
    data_with_categories_and_subcategories["category"] = data_with_categories_and_subcategories["subcategory"].apply(categorize_subcategory)

    return data_with_categories_and_subcategories

def calculate_ingredient_proportion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes the proportion of each ingredient in a recipe.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset containing recipe ingredients and their quantities.

    Returns:
    --------
    pd.DataFrame
        The DataFrame with an additional 'Ingredient_Proportion' column.

    Example:
    --------
    >>> data = {'Recipe_Index': ['R1', 'R1', 'R2'], 'Ingredient': ['flour', 'sugar', 'butter'], 'Quantity': [200, 100, 50]}
    >>> df = pd.DataFrame(data)
    >>> df = calculate_ingredient_proportion(df)
    >>> print(df[['Recipe_Index', 'Ingredient', 'Ingredient_Proportion']])
    """
    df['total_quantity'] = df.groupby('Recipe_Index')['Quantity'].transform('sum')
    df['Ingredient_Proportion'] = df['Quantity'] / df['total_quantity']
    df.drop(columns=['total_quantity'], inplace=True)
    return df

def calculate_ingredient_popularity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and normalizes the popularity score for each ingredient based on its occurrence across recipes.

    Formula:
        Raw Popularity = (Number of Recipes Containing Ingredient) / (Total Recipes)
        Normalized Popularity = (Raw Popularity - min) / (max - min)

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset containing ingredient information.

    Returns:
    --------
    pd.DataFrame
        The DataFrame with an additional 'Popularity_Score' column (normalized between 0 and 1).

    Example:
    --------
    >>> data = {'Recipe_Index': ['R1', 'R1', 'R2', 'R2', 'R2'], 'Ingredient': ['flour', 'sugar', 'butter', 'milk', 'vanilla']}
    >>> df = pd.DataFrame(data)
    >>> df = calculate_ingredient_popularity(df)
    >>> print(df[['Ingredient', 'Popularity_Score']].drop_duplicates())
    """
    # Count how many unique recipes contain each ingredient
    ingredient_counts = df.groupby('Ingredient')['Recipe_Index'].nunique()

    # Normalize the popularity score between 0 and 1
    min_count = ingredient_counts.min()
    max_count = ingredient_counts.max()
    ingredient_counts = (ingredient_counts - min_count) / (max_count - min_count)

    # Merge back to the original DataFrame
    df = df.merge(ingredient_counts.rename("Popularity_Score"), on="Ingredient")

    return df

def calculate_complexity_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a normalized complexity score based on the number of unique ingredients per recipe.

    The complexity score is calculated as:
        (num_ingredients - min(num_ingredients)) / (max(num_ingredients) - min(num_ingredients))

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset containing recipes and their ingredients.

    Returns:
    --------
    pd.DataFrame
        The DataFrame with an additional 'Complexity_Score' column.

    Example:
    --------
    >>> data = {'Recipe_Index': ['R1', 'R1', 'R2', 'R2', 'R2'], 'Ingredient': ['flour', 'sugar', 'butter', 'milk', 'vanilla']}
    >>> df = pd.DataFrame(data)
    >>> df = calculate_complexity_score(df)
    >>> print(df[['Recipe_Index', 'Complexity_Score']].drop_duplicates())
    """
    # Count the number of unique ingredients per recipe
    ingredient_counts = df.groupby('Recipe_Index')['Ingredient'].nunique()

    # Normalize complexity score between 0 and 1
    min_count = ingredient_counts.min()
    max_count = ingredient_counts.max()
    ingredient_counts = (ingredient_counts - min_count) / (max_count - min_count)

    # Merge back to the original DataFrame
    df = df.merge(ingredient_counts.rename("Complexity_Score"), on="Recipe_Index")

    return df

def main():
    """
    Reads in the raw data from the web and saves it to data/raw/raw_cookie_data.csv.
    Proccesses the raw data by generating the missing rating values.
    Engineers new features: ingredient category, ingredient subcategory, 
    ingredient proportion, ingredient popularity score, and complexity score.
    Saves the processed data to data/processed/processed_cookie_data.csv.
    """
    # read data from web
    raw_data = read_data()

    # save raw data to csv
    raw_data.to_csv("data/raw/raw_cookie_data.csv")

    # Engineer ingredient categories and subcategories
    processed_data = engineer_categories_and_subcategories(raw_data)

    # Compute ingredient proportion
    processed_data = calculate_ingredient_proportion(processed_data)

    # Compute ingredient popularity score
    processed_data = calculate_ingredient_popularity(processed_data)

    # Compute complexity score using the 'Text' column
    processed_data = calculate_complexity_score(processed_data)

    # Save processed data a csv file
    processed_data.to_csv("data/processed/processed_cookie_data.csv")

    # Save the processed data as a parquet file
    processed_data.to_parquet("data/processed/processed_cookie_data.parquet")

if __name__ == "__main__":
    main()
