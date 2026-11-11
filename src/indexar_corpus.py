import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

corpus = [ 
    "La aplicación cliente toma los datos de un tramo de linea desde el terreno y los almacena localmente.",
    "Usando los datos almacenados de un tramo, se calcula la tensión y deformación de la linea "
    "para diferentes condiciones ambientales.",
    "Desde la normativa técnica y especificaciones del cable, se obtiene valores y rangos limite de diseño.",
    "Verificar que la tensión y deformación cumpla con los limites de diseño y calcular el "
    "coeficiente de seguridad de la linea.",
    "Solicita al usuario un re-diseño sino se cumple con los limites o el coeficiente de es muy bajo, "
    "en caso contrario la aplicación sube los datos del tramo a la nube para su almacenamiento."
]

splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.create_documents(corpus)
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./vectorstore",
)

print(f"Indexados {len(chunks)} chunks en ./vectorstore")



