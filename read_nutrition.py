import json

# Path to the JSON file
file_path = 'food_data.json'

# Open and read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Access the SurveyFoods list
survey_foods = data['SurveyFoods']

# Iterate through each food item and print the description and calories



# Access the SurveyFoods list

def getCalandMacros(description):
    for food in survey_foods:
        if description == food['description']:
            calories = next((nutrient['amount'] for nutrient in food['foodNutrients'] if nutrient['nutrient']['name'] == 'Energy'), None)
            protein = next((nutrient['amount'] for nutrient in food['foodNutrients'] if nutrient['nutrient']['name'] == 'Protein'), None)
            fat = next((nutrient['amount'] for nutrient in food['foodNutrients'] if nutrient['nutrient']['name'] == 'Total lipid (fat)'), None)
            carb = next((nutrient['amount'] for nutrient in food['foodNutrients'] if nutrient['nutrient']['name'] == 'Carbohydrate, by difference'), None)
            return calories, protein, fat, carb
    return None

