# -*- coding: utf-8 -*-
"""loading and fastAPI

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aZHpAfmmmYUxNShsrqBfBeB21snYd6bk
"""

!pip install gradio fastapi

!pip install pyngrok uvicorn nest_asyncio

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import nest_asyncio
import uvicorn
from pyngrok import ngrok


ngrok.set_auth_token("2kTkJ2J0Un348hrSBFGtp3H3FJS_4rZY41YdzHdqtngtqR4KR")

app = FastAPI()

class InputData(BaseModel):
    gender: str
    age: str
    hypertension: str
    heart_disease: str
    smoking_history: str
    bmi: str
    HbA1c_level: str
    blood_glucose_level: str

def preprocess_input(data: InputData):
    gender = 0 if data.gender == "Male" else 1

    age_map = {
        "child": 0,
        "young": 1,
        "adult": 2,
        "old": 3,
        "very old": 4
    }
    age = age_map.get(data.age, 2)

    hypertension = 0 if data.hypertension == "No" else 1
    heart_disease = 0 if data.heart_disease == "No" else 1

    smoking_map = {
        "never": 0,
        "No Info": 1,
        "current": 2,
        "former": 3,
        "ever": 4
    }
    smoking_history = smoking_map.get(data.smoking_history, 1)

    bmi_map = {
        "underweight": 0,
        "normal": 1,
        "overweight": 2,
        "obese": 3,
        "very obese": 4
    }
    bmi = bmi_map.get(data.bmi, 1)

    HbA1c_map = {
        "low": 0,
        "normal": 1,
        "high": 2,
        "very high": 3
    }
    HbA1c_level = HbA1c_map.get(data.HbA1c_level, 1)

    glucose_map = {
        "low": 0,
        "normal": 1,
        "high": 2,
        "very high": 3
    }
    blood_glucose_level = glucose_map.get(data.blood_glucose_level, 1)

    return [[gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level]]

@app.post("/predict/")
async def predict(data: InputData):
    processed_data = preprocess_input(data)
    prediction = DT_diabetes_model.predict(processed_data)
    result = "Positive" if int(prediction[0]) == 1 else "Negative"
    return {"prediction": result}

if __name__ == "__main__":
    # Start ngrok tunnel for public URL
    ngrok_tunnel = ngrok.connect(8000)
    print('Public URL:', ngrok_tunnel.public_url)

    # Apply nested asyncio to allow running asyncio event loop
    nest_asyncio.apply()

    # Run the FastAPI application
    uvicorn.run(app, port=8000)

!pip install gradio

import gradio as gr
import requests

# Load the trained model
model = joblib.load('/content/drive/MyDrive/models/DT_model_diabetes.sav')


def predict_diabetes(gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level):

    input_data = {
        "gender": gender,
        "age": age,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_history": smoking_history,
        "bmi": bmi,
        "HbA1c_level": HbA1c_level,
        "blood_glucose_level": blood_glucose_level
    }

    # Send a POST request to the FastAPI endpoint
    response = requests.post("http://127.0.0.1:8000/predict/", json=input_data)

    # Check if the request was successful
    if response.status_code == 200:
        prediction = response.json()["prediction"]
        return f"Model Prediction is: {prediction}"
    else:
        return "Error: Unable to get prediction from the model."

with gr.Blocks() as demo:
    with gr.Row():
        gender = gr.Dropdown(["Male", "Female"], label="Gender")
        age = gr.Dropdown(["child", "young", "adult", "old", "very old"], label="Age")
        hypertension = gr.Dropdown(["Yes", "No"], label="Hypertension")
        heart_disease = gr.Dropdown(["Yes", "No"], label="Heart Disease")
    with gr.Row():
        smoking_history = gr.Dropdown(["never", "No Info", "current", "former", "ever"], label="Smoking History")
        bmi = gr.Dropdown(["underweight", "normal", "overweight", "obese", "very obese"], label="BMI")
        HbA1c_level = gr.Dropdown(["low", "normal", "high", "very high"], label="HbA1c Level")
        blood_glucose_level = gr.Dropdown(["low", "normal", "high", "very high"], label="Blood Glucose Level")

    btn = gr.Button("Predict")
    output = gr.Textbox(label="Model Prediction")

    btn.click(fn=predict_diabetes,
             inputs=[gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level],
             outputs=output)

demo.launch()

