from consumir_API_Gemini_Lite import prueba_de_conexion

pregunta = "Explica qué es una API en términos simples."
system_instruction = "Eres un asistente técnico. Responde siempre en un máximo de 3 oraciones."
print(prueba_de_conexion(pregunta, system_instruction))

