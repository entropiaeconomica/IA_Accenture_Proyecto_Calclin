from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.7)

# Paso 1: Extraer ideas clave del texto
plantilla_extraccion = PromptTemplate.from_template(
    "Lee el siguiente texto y devuelve 5 ideas relevantes que puedas obtener de este. "
    "Entrega estas ideas en forma de lista, cada idea en una linea de no mas de 12 palabras:\n\n{texto}")
paso_extraccion = plantilla_extraccion | modelo | StrOutputParser()

# Paso 2: Reescribir en lenguaje sencillo
plantilla_simplificacion = PromptTemplate.from_template(
    "Resume la siguiente lista de ideas en un parrafo de no mas de 100 palabras, "
    "en lenguaje no cientifico y que pueda dar una visión clara del tema a quien lo lea:\n\n{lista}")
paso_simplificacion = plantilla_simplificacion | modelo | StrOutputParser()

# Paso 3: formatear como lista
plantilla_formato = PromptTemplate.from_template(
    "A partir del siguiente parrafo obtiene una lista de viñetas markdown, "
    "de máximo 5 líneas, sin introducción:\n\n{parrafo}")
paso_formato = plantilla_formato | modelo | StrOutputParser()

texto_entrada = (
    "El diseño sismorresistente aplica la dinámica estructural y "
    "la ingeniería geotécnica para que los edificios soporten terremotos sin colapsar. "
    "Se basa en las leyes de Newton: el movimiento del suelo genera fuerzas inerciales "
    "proporcionales a la masa de la estructura y a su aceleración sísmica. "
    "Los ingenieros analizan el periodo natural de vibración del edificio para "
    "evitar la resonancia con las ondas del suelo y del tipo de terreno. "
    "Además, diseñan elementos dúctiles y sistemas de disipación o aislamiento "
    "que absorben energía sísmica mediante deformaciones controladas, protegiendo vidas y "
    "permitiendo reparaciones tras sismos severos."
)

# Paso 1 Extraccion
lista = paso_extraccion.invoke({"texto": texto_entrada})
print(lista)
print(type(lista))

# Paso 2 Simplificacion
parrafo = paso_simplificacion.invoke({"lista": lista})
print(parrafo)
print(type(parrafo))

# Paso 3 Formateo
resultado = paso_formato.invoke({"parrafo": parrafo})
print(resultado)
print(type(resultado))

cadena =(
    plantilla_extraccion | modelo | StrOutputParser() | (lambda lista: {"lista": lista}) | 
    plantilla_simplificacion | modelo | StrOutputParser() | (lambda parrafo: {"parrafo": parrafo}) | 
    plantilla_formato | modelo | StrOutputParser())

respuesta = cadena.invoke({"texto": texto_entrada})
print(respuesta)



