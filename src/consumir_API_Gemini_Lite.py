import requests
import json
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()

response_schema = {
	"type": "OBJECT",
	"properties": {
    	"categories": { "type": "STRING" },
    	"confianza": { "type": "NUMBER" }
	},
	"required": ["categories", "confianza"]
}

def construir_peticion(pregunta: str, system_instruction: str, response_schema=None):
    """
    Esta función construye la petición para la API de Gemini Lite, 
    tiene como parametros la pregunta y las instrucciones del sistema 
    que debe ingresar el usuario.
    """
    if not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía.")
    API_KEY = os.getenv('GEMINI_API_KEY')
    modelo = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    body = {
            "systemInstruction": {
                "parts": [ { "text": system_instruction } ]
            },
            "contents": [
                { "parts": [ { "text": pregunta } ] }
            ]
        }
    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    root = json.dumps(body)
    headers = {'Content-Type': 'application/json', 'x-goog-api-key': API_KEY}
    return url, root, headers

def enviar_peticion(url, root, headers):
    """
    Esta función envía la petición a la API de Gemini Lite y devuelve la 
    respuesta de la API.
    """
    try:
        response = requests.request("POST", url, headers=headers, data=root)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Error de conexión. Por favor, verifica tu conexión a Internet.")
    try:
        respuesta = json.loads(response.text)
    except requests.exceptions.JSONDecodeError:
        raise ValueError("La respuesta no es un JSON válido.")
    return respuesta

def obtener_texto_respuesta(respuesta):
    """
    Esta función obtiene el texto de la respuesta de la API de Gemini Lite.
    """
    try:
        return respuesta['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        raise ValueError("La respuesta no contiene el texto esperado en la posición especificada.")

def calcular_costo_peticion(respuesta, precio_token_pregunta, precio_token_respuesta):
    """
    Esta función calcula el costo de la petición a la API de Gemini Lite.
    """
    metadatos = respuesta['usageMetadata']
    costo_pregunta = metadatos['promptTokenCount'] * precio_token_pregunta
    costo_respuesta = metadatos['candidatesTokenCount'] * precio_token_respuesta
    return costo_pregunta + costo_respuesta

def limpiar_texto(texto):
    """
    Esta función limpia el texto de la respuesta de la API de Gemini Lite.
    """
    # Eliminar saltos de línea y espacios extra
    texto_limpio = re.sub(r'\s+', ' ', texto).strip()
    try:
        data = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("El texto de la respuesta no es un JSON válido.")
    return data

def prueba_de_conexion_sin_esquema(pregunta, system_instruction):
    """
    Esta función prueba la conexión con la API de Gemini Lite y devuelve 
    la respuesta en texto. Calcula e imprime el costo de la petición 
    y el tiempo de respuesta.
    """
    url, root, headers = construir_peticion(pregunta, system_instruction)
    inicio = time.perf_counter()
    respuesta = enviar_peticion(url, root, headers)
    fin = time.perf_counter()
    duracion = fin - inicio
    print(f"Tiempo de respuesta: {duracion:.2f} segundos")
    costo_peticion = calcular_costo_peticion(respuesta, 0.0001, 0.0002)  # Ejemplo de precios por token
    print(f"Costo estimado de la petición: US${costo_peticion:.6f}")
    texto_respuesta = obtener_texto_respuesta(respuesta)
    return texto_respuesta

def prueba_de_conexion_con_esquema(pregunta, system_instruction):
    """
    Esta función prueba la conexión con la API de Gemini Lite y devuelve 
    la respuesta en el formato esperado. Calcula e imprime el costo de la petición 
    y el tiempo de respuesta.
    """
    url, root, headers = construir_peticion(pregunta, system_instruction, response_schema)
    inicio = time.perf_counter()
    respuesta = enviar_peticion(url, root, headers)
    fin = time.perf_counter()
    duracion = fin - inicio
    print(f"Tiempo de respuesta: {duracion:.2f} segundos")
    costo_peticion = calcular_costo_peticion(respuesta, 0.0001, 0.0002)  # Ejemplo de precios por token
    print(f"Costo estimado de la petición: US${costo_peticion:.6f}")
    texto_respuesta = obtener_texto_respuesta(respuesta)
    data_respuesta = limpiar_texto(texto_respuesta)
    return data_respuesta
