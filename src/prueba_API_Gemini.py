import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def request_gemini_api(pregunta):
    API_KEY = os.getenv('GEMINI_API_KEY')
    modelo = "gemini-3.6-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={API_KEY}"
    body = {
        "contents": [
            {"parts": [{"text": pregunta}]}
        ]
    }
    response = requests.post(url, json=body)
    respuesta = response.json()
    return respuesta['candidates'][0]['content']['parts'][0]['text']
print(request_gemini_api("Confirma en una frase corta que esta conexión funciona"))
