import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore_recargado = Chroma(
    persist_directory="./vectorstore",
    embedding_function=embeddings,
)
print(vectorstore_recargado._collection.count())

