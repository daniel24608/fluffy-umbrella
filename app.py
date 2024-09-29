from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import base64
import requests
import json
import csv

app = Flask(__name__)

# Anthropic API endpoint and key
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = "your_api_key_here"  # Replace with your actual API key

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load food descriptions from CSV
def load_food_descriptions():
    food_descriptions = []
    with open('food_descriptions.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            food_descriptions.append(row)
    return food_descriptions

FOOD_DESCRIPTIONS = load_food_descriptions()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image(image_path):
    encoded_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    food_items = ", ".join([food['name'] for food in FOOD_DESCRIPTIONS])
    
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 100,  # Adjust this value as needed
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "Accurately identify food items from user-submitted photos. This means you must MATCH the photo to exactly one of the items in the 'food_descriptions.csv' database. The output should be in the format: [Food Item]: [key for dictionary of csv][Identified food name]."
                    }
                ]
            }
        ],
        "system": "Profession/Role: Food Recognition and Nutrition Assistant; Objective: Your task is to accurately identify food items from user-submitted photos. You must MATCH the photo to exactly one of the items in the 'food_descriptions.csv' database."
    }
    
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        identified_food = response.json()['content'][0]['text'].strip()
        return match_food_description(identified_food)
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def match_food_description(identified_food):
    if identified_food == "No match found":
        return {"match": False, "message": "No matching food item found in the database."}
    
    for food in FOOD_DESCRIPTIONS:
        if food['name'].lower() == identified_food.lower():
            return {"match": True, "food_item": food}
        return {"match": False, "message": f"Identified '{identified_food}', but no exact match found in the database."}
    

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image
            result = process_image(filepath)
            
            # save the result to a text file
            result_filename = f"result_{filename}.txt"
            with open(os.path.join(app.config['UPLOAD_FOLDER'], result_filename), 'w') as f:
               f.write(result)
           
           # Remove the original image file after processing
            os.remove(filepath)
           
            return jsonify({'result': result, 'result_file': result_filename})
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)