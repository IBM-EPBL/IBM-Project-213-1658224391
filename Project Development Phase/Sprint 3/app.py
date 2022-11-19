import flask
from flask import request, render_template
from flask_cors import CORS
import joblib

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
    model=joblib.load('model.pkl')
    species = model.predict(X)[0]
    return render_template('predict.html',predict=species)

if __name__ == '__main__':
    app.run()