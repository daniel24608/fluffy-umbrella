from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import base64
import requests
import json

app = Flask(__name__)

# Anthropic API endpoint and key
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = "your_api_key_here"  # Replace with your actual API key

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,  # Adjust this value as needed
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
                        "text": "Analyze this image and provide a detailed description."
                    }
                ]
            }
        ],
        "system": "You are an expert image analyst. Provide detailed, insightful observations about the image content, focusing on key elements, colors, composition, and any notable features. Your analysis should be thorough and professional."
    }
    
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()['content'][0]['text']
    else:
        return f"Error: {response.status_code}, {response.text}"

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