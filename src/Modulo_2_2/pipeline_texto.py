import re
from collections import Counter
from cliente import consultar_modelo

def limpiar_texto(texto: str) -> str:
    """Normaliza el texto: minúsculas y sin puntuación."""
    if not isinstance(texto, str):
        tipo = type(texto).__name__
        raise TypeError(f"limpiar_texto espera str, no {tipo}")
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def tokenizar(texto_limpio: str) -> list[str]:
    """Convierte texto limpio en una lista de tokens."""
    return texto_limpio.split()

def vectorizar(tokens: list[str]) -> Counter:
    """Cuenta cuántas veces aparece cada token."""
    return Counter(tokens)

def procesar_texto(texto):
    texto_limpio = limpiar_texto(texto)
    return tokenizar(texto_limpio)

consulta = "¿Cuál es la unidad de medida de la temperatura absoluta?"
referencia = "La unidad de medida de la temperatura absoluta es el Kelvin (K)."
respuesta = consultar_modelo(consulta)

unidades_referencia = referencia.split()
unidades_respuesta = respuesta.split()
unidades_comunes = set(unidades_referencia) & set(unidades_respuesta)
if unidades_referencia:
    simil_sin_proceso = len(set(unidades_comunes))/len(set(unidades_referencia))
else:
    simil_sin_proceso = 0.0

tokens_referencia = procesar_texto(referencia)
tokens_respuesta = procesar_texto(respuesta)
tokens_comunes = set(tokens_referencia) & set(tokens_respuesta)
if tokens_referencia:
    simil_con_proceso = len(set(tokens_comunes))/len(set(tokens_referencia))
else:
    simil_con_proceso = 0.0

print(f"[Caso 1] Similitud sin proceso: {simil_sin_proceso:.1%}")

print(f"[Caso 1] Similitud con proceso: {simil_con_proceso:.1%}")



