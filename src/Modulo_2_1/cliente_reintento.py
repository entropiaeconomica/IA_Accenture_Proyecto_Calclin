import time
import random
from typing import Callable, Any

# --- Mock de "enviar_peticion": simula que el proveedor falla las primeras veces ---
intentos_previos = 0

def enviar_peticion(cuerpo: dict) -> dict:
	global intentos_previos
	intentos_previos += 1
	if intentos_previos < 5:
		raise TimeoutError("Límite de peticiones excedido. Hay que esperar y reintentar.")
	return {"contenido": "Respuesta simulada exitosa", "intento": intentos_previos}

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

cuerpo = {"contents": [{"parts": [{"text": "Hola"}]}]}
respuesta = con_reintento(lambda: enviar_peticion(cuerpo))
print(respuesta)




