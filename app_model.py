from flask import Flask, request, jsonify
import os
import pickle
# from sklearn.model_selection import cross_val_score
# import pandas as pd


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. Endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/predict', methods=['GET'])
def predict():
    model = pickle.load(open('ejercicio/data/advertising_model.pkl','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        data = request.get_json()
        input_data = data.get('data', None)
        if input_data is None:
            return "Missing args, the input values are needed to predict"
        else:
            return {"prediction": round(model.predict(input_data)[0],2)}
    else:
        prediction = model.predict([[int(tv),int(radio),int(newspaper)]])
        return {"prediction": round(prediction[0],2)}

app.run()