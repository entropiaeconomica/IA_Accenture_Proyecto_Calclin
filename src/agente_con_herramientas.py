from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import (AgentExecutor, create_tool_calling_agent)
from langchain_core.prompts import (ChatPromptTemplate, MessagesPlaceholder)

load_dotenv()  # Carga las variables de entorno desde un archivo .env

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.7)

@tool
def buscar_en_documentacion(consulta: str) -> str:
    """
    Busca información relevante en la documentación interna del producto.
    Usar cuando la pregunta es sobre cómo funciona algo del sistema.
    """
    documentacion = {
        "reintentos": (
            "El cliente reintenta hasta 3 veces "
            "ante un TimeoutError, con espera "
            "creciente."
        ),
        "costos": (
            "El costo se calcula a partir de "
            "totalTokenCount, según la tarifa "
            "vigente."
        )
    }
    for clave, texto in documentacion.items():
        if clave in consulta.lower():
            return texto
    return "No encontré información para esa consulta."

@tool
def calcular(expresion: str) -> str:
    """
    Evalúa una expresión aritmética simple, como '340 + 215'. 
    Usar cuando la pregunta requiere un cálculo numérico.
    """
    permitido = set("0123456789+-*/(). ")
    if not set(expresion) <= permitido:
        return "Expresión no permitida."
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error al evaluar la expresión: {e}"

herramientas = [buscar_en_documentacion, calcular]

prompt_agente = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente que responde usando las herramientas disponibles cuando las necesites."),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad")
])

agente = create_tool_calling_agent(modelo, herramientas, prompt_agente)

ejecutor_agente = AgentExecutor(agent=agente, tools=herramientas, verbose=True)

#resultado_uno = ejecutor_agente.invoke({"entrada": "¿Cuánto es 340 más 215?"})
#print(resultado_uno["output"])
resultado_dos = ejecutor_agente.invoke({"entrada": "¿Cuántas veces reintenta el cliente ante un error?"})
print(resultado_dos["output"])


