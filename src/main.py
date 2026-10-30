from consumir_API_Gemini_Lite import prueba_de_conexion_con_esquema, prueba_de_conexion_sin_esquema

#pregunta = "Explica qué es una API en términos simples."
pregunta = "Cual es la capital de Chile y como es una descripción de esta ciudad"
system_instruction = "Eres un asistente técnico. Responde siempre en un máximo de 3 oraciones."
print(prueba_de_conexion_sin_esquema(pregunta, system_instruction))
print(prueba_de_conexion_con_esquema(pregunta, system_instruction))




