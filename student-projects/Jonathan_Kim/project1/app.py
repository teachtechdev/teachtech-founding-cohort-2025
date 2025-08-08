from google.colab import drive
import os
import pandas as pd
import joblib
drive.mount('/content/drive', force_remount=True)
MODEL_PATH = '/content/drive/MyDrive/stroke_model.pkl'
def get_user_input():
    print("Personal Information:")
    gender = input("Gender (Male/Female/Other): ")
    age = float(input("Age: "))
    hypertension = int(input("Do you have hypertension? (0 = No, 1 = Yes): "))
    heart_disease = int(input("Do you have any heart disease? (0 = No, 1 = Yes): "))
    ever_married = input("Have you ever been married? (Yes/No): ")
    work_type = input("Work Type (children / Govt_job / Never_worked / Private / Self-employed): ")
    residence_type = input("Residence Type (Urban/Rural): ")
    avg_glucose_level = float(input("Average glucose level: "))
    bmi = float(input("BMI: "))
    smoking_status = input("Smoking status (formerly smoked / never smoked / smokes / Unknown): ")
    return {
        'gender': gender,
        'age': age,
        'hypertension': hypertension,
        'heart_disease': heart_disease,
        'ever_married': ever_married,
        'work_type': work_type,
        'Residence_type': residence_type,
        'avg_glucose_level': avg_glucose_level,
        'bmi': bmi,
        'smoking_status': smoking_status
    }
def generate_note_from_input(user_input):
    note = []
    note.append(f"{user_input['gender']} patient, aged {int(user_input['age'])}.")
    if user_input['hypertension'] == 1:
        note.append("Has a history of hypertension.")
    if user_input['heart_disease'] == 1:
        note.append("Suffers from heart disease.")
    if user_input['ever_married'] == 'Yes':
        note.append("Is married.")
    note.append(f"Works in {user_input['work_type']}.")
    note.append(f"Average glucose level is {user_input['avg_glucose_level']:.1f}.")
    note.append(f"BMI is {user_input['bmi']:.1f}.")
    if user_input['smoking_status'] != 'Unknown':
        note.append(f"Smoking status: {user_input['smoking_status']}.")
    return " ".join(note)
model = joblib.load(MODEL_PATH)
user_data = get_user_input()
user_note = generate_note_from_input(user_data)
prediction = model.predict([user_note])[0]
probability = model.predict_proba([user_note])[0][1]
print("Prediction:")
print(f"Patient Note: {user_note}")
print(f"Stroke Risk: {'HIGH' if prediction == 1 else 'LOW'}")
print(f"Model Probability of Stroke: {probability * 100:.2f}%")
