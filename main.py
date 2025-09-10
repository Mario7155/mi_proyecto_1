import pandas as pd
import requests
import time
import threading
from flask import Flask
import os

# 🔹 Configuración
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQLN4AQYAIb-etfCO_Fvjn62FoCvb4EIsBm28mE1cPiQuGT9wDwfQsEKUiyX0ZdMQ/pub?output=csv"
INSTANCE_ID = "instance142311"
API_KEY = "nk4en5y6x7vv6gdr"

# Endpoint correcto de UltraMsg
API_URL = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

# 🔹 Worker: envía los mensajes una vez
def enviar_mensajes():
    print("🚀 Iniciando envío de mensajes...")
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception as e:
        print(f"❌ Error al leer la hoja: {e}")
        return

    enviados = set()

    for _, row in df.iterrows():
        numero = str(row["numero"])
        mensaje = str(row["mensaje"])

        if numero in enviados:
            continue

        payload = {
            "token": API_KEY,
            "to": numero,
            "body": mensaje
        }

        try:
            response = requests.post(API_URL, data=payload)  # UltraMsg usa form-data
            print(f"✅ Enviado a {numero}: {response.text}")
        except Exception as e:
            print(f"❌ Error con {numero}: {e}")

        enviados.add(numero)
        time.sleep(5)  # ajusta tiempo de espera según tus necesidades

    print("🎉 Todos los mensajes enviados.")

# 🔹 Lanzar worker en un hilo
threading.Thread(target=enviar_mensajes, daemon=True).start()

# 🔹 Flask “dummy” para Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Worker ejecutándose 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
