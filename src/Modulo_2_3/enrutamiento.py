from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableLambda

load_dotenv()

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente parrafo de soporte en una sola "
    "palabra: pregunta, queja o sugerencia. Responde solo "
    "con esa palabra.\n\n{mensaje}"
)

respuesta_generica = RunnableLambda(
    lambda x: (
        "Gracias por tu mensaje. Un miembro de nuestro "
        "equipo te va a responder pronto."
    )
)

def construir_cadena_pregunta(modelo):
    return (
    PromptTemplate.from_template(
        "Responde esta pregunta técnica con precisión:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
    )

def construir_cadena_queja(modelo):
    return (
    PromptTemplate.from_template(
        "Responde a esta queja con empatía, reconociendo el "
        "problema antes de ofrecer una solución:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
    )

def construir_cadena_sugerencia(modelo):
    return (
    PromptTemplate.from_template(
        "Agradece esta sugerencia y explica cómo se evaluará "
        "dentro del producto:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
    )

def construir_paso_clasificacion(modelo):
    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )

def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_queja=None,
    cadena_sugerencia=None,
    cadena_pregunta=None,
):
    cadena_queja = cadena_queja or RunnablePassthrough()
    cadena_sugerencia = cadena_sugerencia or RunnablePassthrough()
    cadena_pregunta = cadena_pregunta or RunnablePassthrough()
    bifurcacion = RunnableBranch(
        (lambda x: x["categoria"] == "queja", cadena_queja),
        (lambda x: x["categoria"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta,
    )
    return (
        RunnablePassthrough.assign(categoria=paso_clasificacion)
        | bifurcacion
    )

def construir_cadena_queja_segura(cadena_queja):
	return cadena_queja.with_fallbacks([respuesta_generica])

def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        print(f"Error procesando mensaje: {error}")
        return (
            "No pudimos procesar tu mensaje en este "
            "momento. Intenta de nuevo más tarde."
        )

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

paso_clasificacion = construir_paso_clasificacion(modelo)
cadena_pregunta = construir_cadena_pregunta(modelo)
cadena_queja = construir_cadena_queja(modelo)
cadena_sugerencia = construir_cadena_sugerencia(modelo)
cadena_con_enrutamiento = construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=cadena_queja,
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
)

respuesta = cadena_con_enrutamiento.invoke({"mensaje": "La app se cierra cuando envio mas de 10 coordenadas geograficas."})
print(respuesta)



