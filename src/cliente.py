from typing import Callable, Any
from cliente_api import construir_peticion, enviar_peticion, obtener_texto_respuesta
import time

def con_reintento(funcion: Callable[[], Any], intentos: int = 5, espera_segundos: int = 2) -> Any:
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except TimeoutError:
            if intento == intentos:
                raise
            print(f"Intento {intento} de {intentos} falló por límite de uso. Reintentando...")
            time.sleep(espera_segundos)

def consultar_modelo(pregunta: str, system_instruction: str = "") -> str:
    cuerpo = construir_peticion(pregunta, system_instruction)
    try:
        respuesta = con_reintento(lambda: enviar_peticion(cuerpo))
    except TimeoutError:
        raise RuntimeError("Se alcanzó el número máximo de intentos. No se pudo obtener una respuesta. Por favor, inténtelo de nuevo más tarde.")
    texto = obtener_texto_respuesta(respuesta)
    return texto

try:
    respuesta = consultar_modelo("¿Cuál es la capital de Chile?")
    print(respuesta)
except ValueError as e:
    print(f"Error de autenticación: {e}")
except RuntimeError as e:
    print(f"Error de límite de uso: {e}")



