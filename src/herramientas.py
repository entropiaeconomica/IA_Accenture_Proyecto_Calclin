from langchain_core.tools import tool

@tool
def buscar_en_documentacion(consulta: str) -> str:
    """Busca información relevante en la
    documentación interna del producto."""
    articulos = {
        "instalación": (
            "Para instalar, corre 'pip install' seguido "
            "del nombre del paquete."
        ),
        "facturación": (
            "La facturación se gestiona desde el panel "
            "de Configuración."
        ),
    }
    for clave, texto in articulos.items():
        if clave in consulta.lower():
            return texto
    return "No encontré información para esa consulta."

@tool
def calcular(expresion: str) -> str:
    """Evalúa una expresión aritmética simple,
    como '340 + 215'. Usar cuando la pregunta
    requiere un cálculo numérico."""
    permitido = set("0123456789+-*/(). ")
    if not set(expresion) <= permitido:
        return "Expresión no permitida."
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error al evaluar la expresión: {e}"


resultado = buscar_en_documentacion.invoke("¿cómo hago la instalación?")
print(resultado)  # Debería imprimir la información sobre instalación
resultado = calcular.invoke("340 * 215")
print(resultado)  # Debería imprimir el resultado del cálculo


