import re
import json
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

def contar_coincidencias(tokens_referencia: list[str], tokens_respuesta: list[str]) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(tokens_referencia: list[str], tokens_respuesta: list[str]) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(tokens_referencia, tokens_respuesta)
    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}
    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)
    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)
    resultado = {"precision": precision, "cobertura": cobertura, "f1": f1}
    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)
    return calcular_precision_cobertura_f1(tokens_referencia, tokens_respuesta)

def media_metricas(resultados):
    if not resultados:
        return {"precision_promedio": 0, "cobertura_promedio": 0, "f1_promedio": 0}
    n = len(resultados)
    return {
        "precision_promedio": sum(r["precision"] for r in resultados) / n,
        "cobertura_promedio": sum(r["cobertura"] for r in resultados) / n,
        "f1_promedio": sum(r["f1"] for r in resultados) / n
        }

casos = [
    (
        "¿Cuántas zonas sísmicas establece la norma chilena NCh433?",
        "Establece tres zonas sísmicas: Zona 1, Zona 2 y Zona 3."
    ),
    (
        "¿Cuál es la aceleración efectiva máxima en Zona Sísmica 3 según NCh433?",
        "La aceleración efectiva máxima Ao es 0,40 g según NCh433."
    ),
    (
        "¿Cuál es el desplazamiento relativo máximo de entrepiso permitido por NCh433?",
        "El desplazamiento relativo máximo es 0,002 veces la altura de entrepiso."
    ),
    (
        "¿Qué decreto supremo modificó la clasificación de suelos de la NCh433?",
        "El Decreto Supremo DS61 MINVU de 2011 modificó la clasificación sísmica."
    ),
    (
        "¿Qué parámetro geotécnico define los tipos de suelo en el DS61?",
        "La velocidad promedio de ondas de corte Vs30 en treinta metros."
    ),
    (
        "¿Cuál es la deriva máxima en el último nivel según el DS61?",
        "El desplazamiento lateral máximo en cubierta es 0,001 veces la altura."
    ),
    (
        "¿Cuál es el porcentaje mínimo de masa sísmica modal según NCh433?",
        "Se exige al menos el 90% de la masa total."
    ),
    (
        "¿Qué norma chilena regula las combinaciones de carga para diseño estructural?",
        "La norma chilena NCh3171 establece las disposiciones generales y combinaciones."
    ),
    (
        "¿Cuál es el factor de carga muerta en combinación última NCh3171?",
        "El factor de mayoración es 1,2 D en combinaciones con sobrecarga."
    ),
    (
        "¿Qué norma chilena establece las sobrecargas de uso en edificios?",
        "La norma NCh1537 regula las cargas permanentes y sobrecargas de uso."
    ),
    (
        "¿Cuál es la sobrecarga mínima para dormitorios de viviendas según NCh1537?",
        "La sobrecarga mínima uniforme para dormitorios de viviendas es 2,0 kN/m²."
    ),
    (
        "¿Qué norma chilena rige el diseño en hormigón armado?",
        "La norma NCh430, complementada con el Decreto Supremo DS60 MINVU."
    ),
    (
        "¿Qué grados de acero de refuerzo establece la norma NCh204?",
        "Establece los grados A440-280H y A630-420H para barras con resaltes."
    ),
    (
        "¿Cuál es la resistencia cilíndrica mínima del hormigón estructural según DS60?",
        "La resistencia cilíndrica mínima especificada f'c debe ser 17 MPa."
    ),
    (
        "¿Qué norma chilena regula las cargas de viento en estructuras?",
        "La norma NCh432 regula el cálculo de la acción del viento."
    ),
    (
        "¿Qué norma chilena establece el cálculo de cargas de nieve?",
        "La norma NCh431 establece las cargas de nieve en techumbres."
    ),
    (
        "¿Qué norma chilena regula el diseño de estructuras de acero?",
        "La norma NCh427 regula el cálculo de estructuras de acero."
    ),
    (
        "¿Qué norma chilena establece el diseño estructural en madera?",
        "La norma NCh1198 regula el cálculo de construcciones en madera."
    ),
    (
        "¿Qué norma chilena regula el diseño de albañilería confinada?",
        "La norma NCh2123 regula el diseño y cálculo de albañilería confinada."
    ),
    (
        "¿Cuál es el factor de importancia para edificios esenciales según NCh433?",
        "Para edificios de Categoría IV el factor de importancia es 1,2."
    )
]

resultados = []
for consulta, referencia in casos:
    respuesta = consultar_modelo(consulta)
    metricas = calcular_metricas(referencia, respuesta)
    resultados.append({
        "consulta": consulta,
        "referencia": referencia,
        "respuesta": respuesta,
        **metricas,
    })

with open("./src/Modulo_2_2/resultados_metricas.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados, archivo, indent=2, ensure_ascii=False)

print(media_metricas(resultados))

casos_orden_creciente = sorted(resultados, key=lambda r: r["f1"])
casos_a_revisar = casos_orden_creciente[:5] + casos_orden_creciente[-5:]
for caso in casos_a_revisar:
    print(caso["consulta"], caso["f1"])



