from fastapi import FastAPI, HTTPException
import sqlite3
import pickle
import uvicorn
import pandas as pd

app = FastAPI()

conn = sqlite3.connect('DataAdvertising.db')
cursor = conn.cursor()

@app.get('/')
async def home():
    return "Bienvenido a mi API del modelo advertising"

# Ruta para obtener todos los libros
@app.get("/v1/sales")
async def get_all():
    def sql_query(query):

        # Ejecuta la query
        cursor.execute(query)

        # Almacena los datos de la query 
        ans = cursor.fetchall()

        # Obtenemos los nombres de las columnas de la tabla
        names = ['tv', 'radio', 'newspaper', 'sales']

        return pd.DataFrame(ans,columns=names)
    
    query = '''
            SELECT * 
            FROM DataAdvertising;
            '''

    df = sql_query(query)
    return df

# Endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada

@app.get("/v1/predict")

async def predictv1(tv: int = None, radio: int = None, newspaper: int = None):

    if tv is None or radio is None or newspaper is None:
        raise HTTPException(status_code=400, detail="Missing args, the input values are needed to predict")
    else:
        model = pickle.load(open('data/advertising_model.pkl', 'rb'))
        prediction = model.predict([[tv, radio, newspaper]])
        return {"prediction": round(prediction[0], 2)}
    
# Endpoint para almacenar nuevos registros en la base de datos

@app.post("/ingest")
async def ingest(data: dict):

    for x in data["data"]:


        if data and 'data' in data:
            
            cursor.execute('''INSERT INTO DataAdvertising (tv, radio, newspaper, sales)
                            VALUES (?,?,?,?)''', (x[0], x[1], x[2], x[3])
                            )
            
            conn.commit()
            return {'message': 'Datos ingresados correctamente'}
        else:
            raise HTTPException(status_code=400, detail="Missing args, the input values are needed to ingest")

@app.get('/predict')
async def predict(data: dict):
    if data and 'data' in data:
        model = pickle.load(open('data/advertising_model.pkl', 'rb'))

        return { "prediction": (model.predict([[data["data"][0][0], data["data"][0][1], data["data"][0][2]]])[0]).round(2)} 
    else:
        return "Es necesario algún dato adicional"

# Endpoint para reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan
@app.post("/retrain")
async def retrain():

    # Con esta función leemos los datos y lo pasamos a un DataFrame de Pandas
    def sql_query(query):

        # Ejecuta la query
        cursor.execute(query)

        # Almacena los datos de la query 
        ans = cursor.fetchall()

        # Obtenemos los nombres de las columnas de la tabla
        names = ['tv', 'radio', 'newspaper', 'sales']

        return pd.DataFrame(ans,columns=names)
    
    query = '''
            SELECT * 
            FROM DataAdvertising;
            '''

    df = sql_query(query)

    Xtrain = df[['tv','radio','newspaper']]
    ytrain = df['sales']
    model = pickle.load(open('data/advertising_model.pkl', 'rb'))

    model.fit(Xtrain, ytrain)
    with open('data/advertising_model.pkl', 'wb') as file:
        pickle.dump(model,file)

    return {'message': 'Modelo reentrenado correctamente.'}



# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)