## AdvertisingAPI

# Predicción de Ventas según Inversión en Publicidad

Este repositorio contiene una API desarrollada con FastAPI para predecir las ventas en función de la inversión en publicidad en tres medios: TV, radio y periódico.

## Uso

1. Clona este repositorio:

https://github.com/NicoUIcreator/AdvertisingAPI.git

2. Instala las dependencias:

pip install -r requirements.txt

3. Ejecuta la API localmente:

uvicorn main:app_model --reload

4. Accede a la documentación de la API en tu navegador:

http://localhost:8000/predict


5. Realiza una solicitud POST con los datos de inversión en publicidad para obtener una predicción de ventas:

```json
{
  "tv": 200,
  "radio": 100,
  "newspaper": 50
}

Contribución
Si deseas contribuir, ¡estamos abiertos a sugerencias y mejoras! Siéntete libre de abrir un issue o enviar un pull request.

Licencia
Este proyecto está bajo la Licencia MIT. 