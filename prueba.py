import flask
import json
import sqlite3
import pandas as pd
import requests  # Importar requests
import pickle
model = pickle.load(open('data/advertising_model.pkl','rb'))

app = flask.Flask(__name__)

conn = sqlite3.connect("ad_data.db")
cursor = conn.cursor()

@app.route("/predict", methods=["POST"])
def predict():
    # Recibir datos de la petición
    data = requests.get_json()
    tv_spend = data["tv_spend"]
    radio_spend = data["radio_spend"]
    newspaper_spend = data["newspaper_spend"]

    # Realizar la predicción
    prediction = model.predict_sales(tv_spend, radio_spend, newspaper_spend)

    # Devolver la respuesta en formato JSON
    response = {"sales": prediction}
    return flask.jsonify(response)

@app.route("/ingest", methods=["POST"])
def ingest():
    # Recibir datos de la petición
    data = requests.get_json()
    tv_spend = data["tv_spend"]
    radio_spend = data["radio_spend"]
    newspaper_spend = data["newspaper_spend"]
    sales = data["sales"]

    # Almacenar los datos en la base de datos
    cursor.execute(
        "INSERT INTO ad_records (tv_spend, radio_spend, newspaper_spend, sales) VALUES (?, ?, ?, ?)",
        (tv_spend, radio_spend, newspaper_spend, sales),
    )
    conn.commit()

    # Devolver un mensaje de confirmación
    response = {"message": "Record stored successfully"}
    return flask.jsonify(response)

@app.route("/retrain", methods=["POST"])
def retrain():
    # Cargar datos de la base de datos a un DataFrame de Pandas
    data = pd.read_sql("ad_records", conn)

    # Reentrenar el modelo con los datos del DataFrame
    model.retrain(data)

    # Guardar el modelo reentrenado
    model.save_model("model.pkl")

    # Devolver un mensaje de confirmación
    response = {"message": "Model retrained successfully"}
    return flask.jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
