import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def request_gemini_api(pregunta):
    modelo = "gemini-3.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    payload = json.dumps({
    "contents": [
        {
        "parts": [
            {
            "text": pregunta
            }
        ]
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'x-goog-api-key': os.getenv('GEMINI_API_KEY')
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    respuesta = json.loads(response.text)
    return respuesta['candidates'][0]['content']['parts'][0]['text']
print(request_gemini_api("Confirma en una frase corta que esta conexión funciona"))
