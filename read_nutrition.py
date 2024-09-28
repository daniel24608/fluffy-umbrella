import json

# Path to the JSON file
file_path = 'condensed_food_data.json'

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
            calories = food['calories']
            protein = food['protein']
            fat = food['fat']
            carb = food['carb']

            return calories, protein, fat, carb
    return None


