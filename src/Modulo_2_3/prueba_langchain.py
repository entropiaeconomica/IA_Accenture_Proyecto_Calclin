from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

plantilla = PromptTemplate.from_template(
    "Explica el concepto de {tema} en un párrafo, "
    "para alguien que recién empieza en {area}."
)

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.7)

prompt = plantilla.invoke(
    {"tema": "entrelazamiento cuántico", "area": "mecanica cuantica"}
)

respuesta = modelo.invoke(prompt.text)

cadena_simple = plantilla | modelo

respuesta_simple = cadena_simple.invoke(
    {"tema": "entrelazamiento cuántico", "area": "mecanica cuantica"}
)

print(prompt.text)
print(respuesta.content)
print(respuesta_simple.content)










