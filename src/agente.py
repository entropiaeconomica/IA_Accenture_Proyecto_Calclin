from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()

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

prompt_agente = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente que responde preguntas usando las herramientas cuando las necesites."),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad")
])

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.7)
herramientas = [buscar_en_documentacion, calcular]
agente = create_tool_calling_agent(modelo, herramientas, prompt=prompt_agente)
ejecutor_agente = AgentExecutor(agent=agente, tools=herramientas, verbose=True)
resultado = ejecutor_agente.invoke({"entrada": "¿Cuánto es 340 más 215?"})
print(resultado["output"][0]["text"])  # Debería imprimir el resultado del cálculo


