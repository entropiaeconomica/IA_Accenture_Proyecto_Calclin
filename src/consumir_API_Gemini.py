import requests
import json
import os
from dotenv import load_dotenv
import time

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

def calcular_costo_peticion(respuesta, precio_token_pregunta, precio_token_respuesta):
    metadatos = respuesta['usageMetadata']
    costo_pregunta = metadatos['promptTokenCount'] * precio_token_pregunta
    costo_respuesta = metadatos['candidatesTokenCount'] * precio_token_respuesta
    return costo_pregunta + costo_respuesta

def prueba_de_conexion(pregunta):
    url, body, headers = construir_peticion(pregunta)
    inicio = time.perf_counter()
    respuesta = enviar_peticion(url, body, headers)
    fin = time.perf_counter()
    duracion = fin - inicio
    print(f"Tiempo de respuesta: {duracion:.2f} segundos")
    texto_respuesta = obtener_texto_respuesta(respuesta)
    costo_peticion = calcular_costo_peticion(respuesta, 0.0001, 0.0002)  # Ejemplo de precios por token
    return texto_respuesta, costo_peticion

print(prueba_de_conexion("Cual es la capital de Chile?"))

