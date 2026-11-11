import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

def construir_peticion(pregunta: str, system_instruction: str = "") -> dict:
    """
    Esta función construye la petición para la API de Gemini Lite, 
    tiene como parametros la pregunta y las instrucciones del sistema 
    que debe ingresar el usuario.
    """
    if not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía.")
    body = {
            "systemInstruction": {
                "parts": [ { "text": system_instruction } ]
            },
            "contents": [
                { "parts": [ { "text": pregunta } ] }
            ]
        }
    return body

def enviar_peticion(body):
    """
    Esta función envía la petición a la API de Gemini Lite y devuelve la 
    respuesta de la API.
    """
    API_KEY = os.getenv('GEMINI_API_KEY')
    modelo = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    headers = {'Content-Type': 'application/json', 'x-goog-api-key': API_KEY}
    try:
        root = json.dumps(body)
        respuesta = requests.request("POST", url, headers=headers, data=root, timeout=10)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        raise TimeoutError("No se pudo contactar al proveedor. Puede ser momentáneo.")
    if respuesta.status_code in (401, 403):
        raise ValueError("Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY.")
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise TimeoutError("El proveedor no pudo procesar la petición. Hay que esperar y reintentar.")
    respuesta.raise_for_status()
    return respuesta.json()

def obtener_texto_respuesta(respuesta):
    """
    Esta función obtiene y limpia el texto de la respuesta de la API.
    """
    try:
        texto = respuesta['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        raise ValueError("La respuesta no contiene el texto esperado en la posición especificada.")
    return texto






    
