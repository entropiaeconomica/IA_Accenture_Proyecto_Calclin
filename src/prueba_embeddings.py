import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Cargar las variables del archivo .env
load_dotenv()

# Verificar la clave antes de llamar a la API
if not os.environ.get("GEMINI_API_KEY"):
    raise SystemExit('Falta GEMINI_API_KEY. Defínela en tu archivo ".env" y vuelve a ejecutar.')

# Inicializar el modelo de embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Llamar a la API e informar con claridad cualquier fallo
try:
    vector = embeddings.embed_query("El cliente reintenta ante un error")
except Exception as error:
    mensaje = str(error)
    if "429" in mensaje or "RESOURCE_EXHAUSTED" in mensaje:
        print("Límite de peticiones alcanzado. Espera un minuto y vuelve a ejecutar.")
    elif "API key" in mensaje or "401" in mensaje or "403" in mensaje:
        print('La API rechazó tu clave. Revisa el valor de GEMINI_API_KEY en tu ".env".')
    else:
        print("No se pudo generar el embedding:", type(error).__name__)
    print("Detalle técnico:", mensaje)
    raise SystemExit(1)

# Mostrar el resultado
print(len(vector))
print(vector[:5])

# Instanciar el vector store guardando la base de datos localmente
vector_store = Chroma(
    collection_name="ejemplo_rag",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Guardar un fragmento de texto (chunk) en el vector store
vector_store.add_texts(["El cliente realiza hasta tres reintentos en caso de error de red."])
print("Chunk guardado exitosamente en Chroma.")




