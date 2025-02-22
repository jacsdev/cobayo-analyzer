import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configura tu API Key
api_key = os.getenv("API_KEY")
openai.api_key = api_key

# Define mensajes cortos y optimizados
messages = [
    {"role": "system", "content": "Responde claro y breve."},
    {"role": "user", "content": "Explica Flask en 2 líneas."}
]

# Llamada a la API con parámetros optimizados
response = openai.ChatCompletion.create(
    model="gpt-4",  # Modelo válido de OpenAI
    messages=messages,
    max_tokens=100,  # Limita la cantidad de tokens generados
    temperature=0.2,  # Evita respuestas creativas innecesarias
    stop=["\n"],  # Corta la respuesta en la primera línea nueva
)

# Imprime la respuesta y tokens usados
print("Respuesta:", response["choices"][0]["message"]["content"])
print("Tokens usados:", response["usage"])