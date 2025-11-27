import pandas as pd
import re

"""
===================================================================
HELPER FUNCTIONS 
===================================================================
"""

def parse_nutrition(nutrition_str):
    """
    Parses the nutrition string into a dictionary of nutrient values.
    """
    if not isinstance(nutrition_str, str): 
        return {}
    
    nutrients = {}
    pattern = re.compile(r'([A-Za-z\s]+)\s([\d.]+)(g|mg)')
    matches = pattern.findall(nutrition_str)
    
    for match in matches:
        nutrient_name = match[0].strip()
        value = float(match[1])
        nutrients[nutrient_name] = value
        
    return nutrients

def calculate_calories(row):
    """
    Calculates estimated calories for a recipe using the 4-4-9 formula.
    """
    try:
        fat_grams = row.get('Total Fat', 0)
        carb_grams = row.get('Total Carbohydrate', 0)
        protein_grams = row.get('Protein', 0)
        return (fat_grams * 9) + (carb_grams * 4) + (protein_grams * 4)
    except (TypeError, KeyError):
        return None

def parse_ingredients(ingredients_str):
    """
    Parses the ingredients string into a list of individual ingredients.
    """
    if not isinstance(ingredients_str, str): 
        return []
    return [item.strip() for item in ingredients_str.split(',')]

"""
===================================================================
THE MAIN RECOMMENDATION ENGINE (MODIFIED FOR CROWD RANKING)
===================================================================
"""

def recommend_recipes(df, user_preferences):
    """
    Cleans, filters, and ranks recipes based on user preferences.
    """
    working_df = df.copy()

    print("Recommendation engine started.")
    print(f"User preferences: {user_preferences}")

    # --- Step 1: Prepare the Data ---
    nutrition_data = working_df['nutrition'].apply(parse_nutrition).apply(pd.Series)
    working_df['calories'] = nutrition_data.apply(calculate_calories, axis=1)
    working_df['ingredients_list'] = working_df['ingredients'].apply(parse_ingredients)

    # --- Step 2: Apply Filters (Knowledge-Based System) ---
    # KBS: Apply filters based on user preferences like calorie count and allergies
    max_calories = user_preferences.get('max_calories')
    if max_calories:
        print(f"Filtering for recipes with less than {max_calories} estimated calories.")
        working_df = working_df.dropna(subset=['calories'])
        working_df = working_df[working_df['calories'] <= max_calories]

    allergies = user_preferences.get('allergies')
    if allergies:
        print(f"Filtering out recipes containing allergens: {allergies}")
        def contains_allergen(ingredients, allergens):
            return any(allergen.lower() in ingredient.lower() for allergen in allergens for ingredient in ingredients)
        working_df = working_df[~working_df['ingredients_list'].apply(lambda x: contains_allergen(x, allergies))]

    # --- Step 3: Rank Recipes (Crowd Recommendation) ---
    # Crowd Recommendation: Rank recipes first by pantry match, then by crowd rating (recipe ratings)
    pantry = user_preferences.get('pantry')
    if pantry and len(pantry) > 0:
        print(f"Ranking recipes by pantry match and crowd rating.")
        
        # Function to calculate pantry match score
        def calculate_pantry_match(ingredients, user_pantry):
            return sum(1 for item in user_pantry if any(item.lower() in ingredient.lower() for ingredient in ingredients))

        working_df['pantry_match_score'] = working_df['ingredients_list'].apply(lambda x: calculate_pantry_match(x, pantry))
        
        # **The key change is here for Crowd Recommendation**
        # First, sort by how many pantry ingredients match.
        # Second, for recipes with the same match score, sort by the public rating.
        working_df = working_df.sort_values(by=['pantry_match_score', 'rating'], ascending=[False, False])
    else:
        # If the user has no pantry, just rank by the crowd's rating
        print("No pantry items provided. Ranking by crowd rating.")
        working_df = working_df.sort_values(by='rating', ascending=False)

    return working_df

"""
===================================================================
TESTING BLOCK 
===================================================================
"""

if __name__ == '__main__':
    try:
        # Assuming you have a dataset of recipes with relevant columns
        raw_df = pd.read_csv('data/recipes_600dataset.csv')

        # Sample user preferences
        sample_user_prefs = {
            'health_goal': 'weight_loss',
            'max_calories': 500,  # Using 500 to get a broader range of results
            'allergies': ['walnut'],
            'pantry': ['chicken', 'onion', 'garlic']  # User has these items
        }
        
        recommendations = recommend_recipes(raw_df, sample_user_prefs)
        
        print(f"\n--- Found {len(recommendations)} Recipes ---")
        print("Showing top results ranked by pantry match and then by rating:")

        # Display the relevant columns to verify the ranking
        display_cols = ['recipe_name', 'pantry_match_score', 'rating', 'calories']
        top_recipes = recommendations[display_cols].head(10).reset_index(drop=True)  # Show top 10 recipes
        print(top_recipes.to_string(index=True))

        # --- Display Ingredients and Directions for the Top 1 Recipe ---
        top_recipe = recommendations.head(1)  # Get the top 1 recipe
        print("\n--- Top Recipe Ingredients and Directions ---")
        
        # Make sure the columns 'ingredients' and 'directions' exist in your dataset
        top_recipe_ingredients = top_recipe['ingredients'].values[0]
        top_recipe_directions = top_recipe['directions'].values[0]
        
        print(f"Ingredients: \n{top_recipe_ingredients}")
        print(f"\nDirections: \n{top_recipe_directions}")

    except FileNotFoundError:
        print("\nError: 'data/recipes_600dataset.csv' not found.")
        print("Please ensure the dataset is in the 'data' folder.")
