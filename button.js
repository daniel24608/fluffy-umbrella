document.getElementById('macroForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting the usual way

    // Get form values
    const heightFeet = parseFloat(document.getElementById('heightFeet').value);
    const heightInch = parseFloat(document.getElementById('heightInch').value);
    const weight = parseFloat(document.getElementById('weight').value);
    const age = parseInt(document.getElementById('age').value);
    const gender = parseInt(document.getElementById('gender').value);

    // Calculate height in cm and weight in kg
    const heightCm = (heightFeet * 30.48) + (heightInch * 2.54);
    const weightKg = weight * 0.453592;

    // Calculate BMR (Basal Metabolic Rate)
    let bmr;
    if (gender === 1) { // Male
        bmr = (10 * weightKg) + (6.25 * heightCm) - (5 * age) + 5;
    } else { // Female
        bmr = (10 * weightKg) + (6.25 * heightCm) - (5 * age) - 161;
    }

    // Assuming moderate activity for calorie calculations (activity factor = 1.55)
    const calories = bmr * 1.55;

    // Calculate macronutrients based on total calories
    const carbohydrates = (0.5 * calories) / 4; // 50% of calories, 4 calories per gram
    const proteins = (0.3 * calories) / 4; // 30% of calories, 4 calories per gram
    const fats = (0.2 * calories) / 9; // 20% of calories, 9 calories per gram

    // Display results in the result section
    document.getElementById('calories').innerText = `Daily Calories: ${calories.toFixed(2)}`;
    document.getElementById('carbs').innerText = `Carbohydrates: ${carbohydrates.toFixed(2)}g`;
    document.getElementById('proteins').innerText = `Proteins: ${proteins.toFixed(2)}g`;
    document.getElementById('fats').innerText = `Fats: ${fats.toFixed(2)}g`;

    // Make the result section visible
    document.getElementById('results').style.display = 'block';
});
