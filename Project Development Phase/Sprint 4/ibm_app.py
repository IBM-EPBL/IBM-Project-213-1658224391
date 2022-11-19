import flask
from flask import request, render_template
from flask_cors import CORS
import joblib

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YeR_HFrqUOtVOM0cIcdQwFyHpjtDwehEpQQE0KG370_b"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predictSpecies():
    ph=float(request.form['ph'])
    Hardness=float(request.form['Hardness'])
    Solids=float(request.form['Solids'])
    Chloramines=float(request.form['Chloramines'])
    Sulfate=float(request.form['Sulfate'])
    Conductivity=float(request.form['Conductivity'])
    Organic_carbon=float(request.form['Organic_carbon'])
    Trihalomethanes=float(request.form['Trihalomethanes'])
    Turbidity=float(request.form['Turbidity'])
    X=[[ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity]]

    payload_scoring = {"input_data": [{"field": [['ph','Hardness','Solids','Chloramines','Sulfate','Conductivity','Organic_carbon','Trihalomethanes','Turbidity']], "values":X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/16f81779-1bbf-45fa-8e34-3f5da54a7a43/predictions?version=2022-11-19', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print("Final prediction :",predict)

    return render_template('predict.html',predict=predict)

if __name__ == '__main__':
    app.run()