from typing import Callable, Any
import os
import requests
import json
import re
from dotenv import load_dotenv
import time
import random

load_dotenv()

COSTO_POR_1000_TOKENS = 0.002  # valor de referencia, puede ajustarse según el costo real de la API
costo_total_sesion = 0

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

def con_reintento(funcion: Callable[[], Any], intentos: int = 5, espera_base: float = 2, espera_maxima: float = 30) -> Any:
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except TimeoutError:
            if intento == intentos:
                raise
            espera_origen = min(espera_base * (2 ** (intento - 1)), espera_maxima)
            espera_aleatoria = espera_origen + random.uniform(0, espera_origen * 0.1)
            print(f"Intento {intento} de {intentos} falló. Reintentando en {espera_aleatoria:.1f} segundos...")
            time.sleep(espera_aleatoria)

def registrar_costo(respuesta: dict) -> float:
	global costo_total_sesion
	metadatos = respuesta.get("usageMetadata", {})
	total_tokens = metadatos.get("totalTokenCount", 0)
	costo_estimado_consulta = (total_tokens / 1000) * COSTO_POR_1000_TOKENS
	costo_total_sesion = costo_total_sesion + costo_estimado_consulta
	print(f"Operación: {total_tokens} tokens, costo estimado: ${costo_estimado_consulta:.5f} (acumulado: ${costo_total_sesion:.5f})")
	return costo_estimado_consulta

def consultar_modelo(pregunta: str, system_instruction: str = "") -> str:
    cuerpo = construir_peticion(pregunta, system_instruction)
    try:
        respuesta = con_reintento(lambda: enviar_peticion(cuerpo))
    except TimeoutError:
        raise RuntimeError("Se alcanzó el número máximo de intentos. No se pudo obtener una respuesta. Por favor, inténtelo de nuevo más tarde.")
    registrar_costo(respuesta)
    texto = obtener_texto_respuesta(respuesta)
    return texto

if __name__ == "__main__":
    try:
        respuesta = consultar_modelo("¿Cuál es la capital de Chile?")
        print(respuesta)
    except ValueError as e:
        print(f"Error de autenticación: {e}")
    except RuntimeError as e:
        print(f"Error de límite de uso: {e}")






