from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests  # Para enviar mensajes a Telegram

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar la clave de la API de OpenAI
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# Configurar el token y el ID de chat de Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Inicializar Flask
app = Flask(__name__)

# Función para procesar mensajes con OpenAI
def chat(user_message):
    """
    Procesa un mensaje del usuario utilizando OpenAI y devuelve la respuesta.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo válido de OpenAI
            messages=[{"role": "user", "content": user_message}],
            max_tokens=100,  # Limita la cantidad de tokens generados
            temperature=0.2,  # Evita respuestas creativas innecesarias
            stop=["\n"],  # Corta la respuesta en la primera línea nueva
        )
        bot_response = response.choices[0].message.content
        return bot_response
    except Exception as e:
        raise Exception(f"Error al procesar el mensaje: {str(e)}")

# Endpoint para recibir mensajes de Telegram
@app.route("/telegram", methods=["POST"])
def telegram():
    # Obtener el cuerpo de la solicitud como JSON
    try:
        data = request.get_json()  # Interpreta el cuerpo como JSON
        if not data:
            return jsonify({"error": "Cuerpo de la solicitud no válido o vacío"}), 400

        # Obtener el mensaje de Telegram
        message = data.get("message", {}).get("text")

        if not message:
            return jsonify({"error": "Mensaje no válido o vacío"}), 400

        # Procesar el mensaje usando la función chat
        try:
            bot_response = chat(message)  # Llamada directa a la función chat
        except Exception as e:
            app.logger.error(f"Error al procesar el mensaje: {str(e)}")
            return jsonify({"error": "Error al procesar el mensaje"}), 500

        # Enviar la respuesta de vuelta a Telegram
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": bot_response
                },
                timeout=10  # Establece un timeout para la solicitud
            )
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error al enviar mensaje a Telegram: {str(e)}")
            return jsonify({"error": "Error al enviar mensaje a Telegram"}), 500

        return jsonify({"status": "Mensaje procesado y enviado a Telegram"})

    except Exception as e:
        app.logger.error(f"Error en el endpoint /telegram: {str(e)}")
        return jsonify({"error": "Error en el servidor"}), 500

# Endpoint para /chat (disponible para otros usos)
@app.route("/chat", methods=["POST"])
def chat_api():
    # Obtener el mensaje del usuario desde el cuerpo de la solicitud
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "El campo 'message' es requerido"}), 400

    # Procesar el mensaje usando la función chat
    try:
        bot_response = chat(user_message)  # Llamada directa a la función chat
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Punto de entrada para ejecutar la API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)