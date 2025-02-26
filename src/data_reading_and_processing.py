# feature_engineer.py
# authors: Mu (Henry) Ha, Javier Martinez, Stephanie Ta
# date: 2025-02-25

# This script reads in the raw data from the web and saves it to data/raw/raw_cookie_data.csv.
# Then, it proccesses the raw data by generating the missing rating values.
# It also engineers new features: ingredient category, ingredient subcategory, 
# ingredient proportion, ingredient popularity score, and complexity score.
# Also saves the processed data to data/processed/processed_cookie_data.csv.

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
    elif ingredient == chocolate_types:
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
    Engineers the features: ingredient category and subcategory
    """

    return data_with_categories_and_subcategories

def main():
    """
    Reads in the raw data from the web and saves it to data/raw/raw_cookie_data.csv.
    Proccesses the raw data by generating the missing rating values.
    Engineers new features: ingredient category, ingredient subcategory, 
    ingredient proportion, ingredient popularity score, and complexity score.
    Saves the processed data to data/processed/processed_cookie_data.csv.
    """
    raw_data = read_data()
    raw_data.to_csv("../data/raw/raw_cookie_data.csv")



if __name__ == "__main__":
    main()