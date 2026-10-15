from dotenv import load_dotenv  # Importa la función load_dotenv del paquete dotenv
import os  # Importa el módulo os para acceder a las variables de entorno

load_dotenv()  # Carga las variables de entorno desde el archivo .env
print(os.getenv("GEMINI_API_KEY"))  # Imprime el valor de la variable de entorno GEMINI_API_KEY
