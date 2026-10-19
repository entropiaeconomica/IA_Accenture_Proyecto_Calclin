import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def construir_peticion(pregunta):
    if not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía.")
    API_KEY = os.getenv('GEMINI_API_KEY')
    modelo = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    body = json.dumps({"contents": [{"parts": [{"text": pregunta}]}]})
    headers = {'Content-Type': 'application/json', 'x-goog-api-key': API_KEY}
    return url, body, headers

def enviar_peticion(url, body, headers):
    try:
        response = requests.request("POST", url, headers=headers, data=body)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Error de conexión. Por favor, verifica tu conexión a Internet.")
    try:
        respuesta = json.loads(response.text)
    except requests.exceptions.JSONDecodeError:
        raise ValueError("La respuesta no es un JSON válido.")
    return respuesta

def obtener_texto_respuesta(respuesta):
    try:
        return respuesta['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        raise ValueError("La respuesta no contiene el texto esperado en la posición especificada.")

def prueba_de_conexion(pregunta):
    url, body, headers = construir_peticion(pregunta)
    respuesta = enviar_peticion(url, body, headers)
    texto_respuesta = obtener_texto_respuesta(respuesta)
    return texto_respuesta

print(prueba_de_conexion("Cual es la capital de Chile?"))

