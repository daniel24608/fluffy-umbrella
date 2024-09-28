/* 
Macro Calculator
*/

#include <iostream>
#include <iomanip>

using namespace std;

int main() {
    int calories;
    double heightFeet;
    double heightInch;
    double heightCm;
    double weight;
    double weightKg;
    int age;
    int gender;
    int skip;

    cout << "Do you know how many calories you eat? (Enter 1 to skip, enter 2 if no)";
    cin >> skip;
    if (skip != 2) {
        goto jump;
    }
    cout << "Height in feet? (Insert inches after)";
    cin >> heightFeet;
    cout << "Inches?";
    cin >> heightInch;
    //Conversion to CM
    heightCm = (heightFeet * 30.48) + (heightInch * 2.54);

    cout << "Age?";
    cin >> age;

    cout << "Weight (pounds)";
    cin >> weight;
    //Conversion to KG
    weightKg = weight * 0.453592;

    cout << "Enter '1' if male; Enter '2' if female";
    cin >> gender;

    if (gender >= 2) {
        calories = ((10 * weightKg) + (6.25 * heightCm) - (5 * age) - 161);
    }
    else if (gender >= 1) {
        calories = ((10 * weightKg) + (6.25 * heightCm) - (5 * age) + 5);
    }

    //Calculate the Macros
    int carbohydrates;
    int carbohydratesLit;
    int carbohydratesLight;
    int carbohydratesMod;
    int fats;
    int fatsLit;
    int fatsLight;
    int fatsMod;
    int proteins;
    int proteinsLit;
    int proteinsLight;
    int proteinsMod;
    int caloriesLittle;
    int caloriesLightly;
    int caloriesModerate;
    int knownCalories;

    caloriesLittle = calories * 1.2;
    caloriesLightly = calories * 1.375;
    caloriesModerate = calories * 1.55;

    carbohydratesLit = (0.5 * caloriesLittle)/4;
    fatsLit = (0.20 * caloriesLittle)/9;
    proteinsLit = (0.30 * caloriesLittle)/4;

    carbohydratesLight = (0.5 * caloriesLightly)/4;
    fatsLight = (0.20 * caloriesLightly)/9;
    proteinsLight = (0.30 * caloriesLightly)/4;

    carbohydratesMod = (0.5 * caloriesModerate)/4;
    fatsMod = (0.20 * caloriesModerate)/9;
    proteinsMod = (0.30 * caloriesModerate)/4;

    //Jump to here if you know your cals
    int carbsSkip;
    int fatsSkip;
    int proteinsSkip;
    jump: 
    cout << "How many calories do you eat in a day? ( Enter 0 if you do not know ) ";
    cin >> knownCalories;
    //give the known calories macros to follow
    carbsSkip = (0.5 * knownCalories)/4;
    fatsSkip = (0.2 * knownCalories)/9;
    proteinsSkip = (0.3 * knownCalories)/4;
    //format stream
    cout << setprecision(2) << fixed;
    cout << "-------------------------------------------------------------------" << endl;
    cout << "(Ignore if you didn't manually put in your calories)  Your macros are: C: " << carbsSkip << " F: " << fatsSkip << 
    " P: " << proteinsSkip << endl;

    cout << "-------------------------------------------------------------------" << endl;
    cout << "(Ignore below if you did manually enter calories)" << endl;
    cout << "Calories (Little to no exercise): " << caloriesLittle << endl;
    cout << "Macros: C: " << carbohydratesLit << " F: " << fatsLit << " P: " << proteinsLit << endl;
    cout << "Calories (Lightly Active): " << caloriesLightly << endl;
    cout << "Macros: C: " << carbohydratesLight << " F: " << fatsLight << " P: " << proteinsLight << endl;
    cout << "Calories (Moderately active): " << caloriesModerate << endl;
    cout << "Macros: C: " << carbohydratesMod << " F: " << fatsMod << " P: " << proteinsMod << endl;

    return 0;

}