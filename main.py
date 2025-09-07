import pandas as pd
import requests
import time
import threading
from flask import Flask
import os

# 🔹 Configuración
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQLN4AQYAIb-etfCO_Fvjn62FoCvb4EIsBm28mE1cPiQuGT9wDwfQsEKUiyX0ZdMQ/pub?output=csv"
API_KEY = "3bd23448befca374ae3f9b4d0bedf3b21f970645dc90e58d71e479f4c8e8fc04"
API_URL = "https://wasenderapi.com/api/send-message"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# 🔹 Worker: envía los mensajes una vez
def enviar_mensajes():
    df = pd.read_csv(SHEET_URL)
    enviados = set()

    for _, row in df.iterrows():
        numero = str(row["numero"])
        mensaje = str(row["mensaje"])

        if numero in enviados:
            continue

        payload = {"to": numero, "text": mensaje}
        response = requests.post(API_URL, json=payload, headers=HEADERS)

        print(f"Enviado a {numero}: {response.text}")

        enviados.add(numero)
        time.sleep(60)

    print("✅ Todos los mensajes enviados.")

# 🔹 Lanzar worker en un hilo
threading.Thread(target=enviar_mensajes).start()

# 🔹 Flask “dummy” para Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Worker ejecutándose 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
