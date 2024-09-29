from flask import Flask, request, render_template, abort
import os

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    operation = request.form.get('operation')
    heightFeet = request.form.get('heightFeet')
    heightInch = request.form.get('heightInch')
    weight = request.form.get('weight')
    age = request.form.get('age')
    gender = request.form.get('gender')
    minutes = request.form.get('minutes')
    days = request.form.get('days')

    if(operation == 'create'):
        return render_template('macro.html')
    
    return render_template('submit.html')

@app.route('/submit', methods=['GET'])
def result_page():
    
    return render_template('submit.html')

@app.route('/submit', methods=['POST'])
def show_create():
    heightFeet = (int)(request.form.get('heightInFeet'))
    heightInch = (int)(request.form.get('heightInInches'))
    weight = (int)(request.form.get('weight'))
    age = (int)(request.form.get('age'))
    gender = (int)(request.form.get('gender'))
    plan = (int)(request.form.get('plan'))
    days = (int)(request.form.get('days'))
    heightFeet *= 12
    heightInch += heightFeet
    heightInch *= 2.54
    calories = 0
    if (gender == 1): 
        bmr = (10 * weight) + (6.25 * heightInch) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * heightInch) - (5 * age) - 161
    #none
    if(days == 0):
        calories = 1.2 * bmr
    elif(days == 1):
        calories = 1.375 * bmr
    elif(days == 2):
        calories = 1.55 * bmr
    elif(days == 3):
        calories = 1.725 * bmr
    elif(days == 4):
        calories = 1.9 * bmr
    
    if(plan == 0):
        abort(400)
    elif(plan == 1):
        calories = calories - 500
    elif(plan == 2):
        calories =calories - 1000
    elif(plan == 3):
        calories =calories + 500
    elif(plan == 4):
        calories =calories + 1000

    carbohydrates = (0.5 * calories) / 4
    context = {
        'bmr': bmr,
        "carbohydrates": carbohydrates,
        'calories': calories,
    }
    return render_template('macro.html', **context)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No file part', 400
    
    file = request.files['image']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return f'File uploaded successfully: {file.filename}', 200

if __name__ == '__main__':
    app.run(debug=True)