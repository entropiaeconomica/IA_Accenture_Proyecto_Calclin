from consumir_API_Gemini_Lite import prueba_de_conexion

BANCO_DE_PROMPTS = [
    {
        "nombre": "clasificación productos",
        "id": "prompt_001",
        "system_prompt": "Eres un experto en clasificación de productos. Responde clasificando el producto como bueno, malo o neutral.", 
        "user_prompt": "Clasifica el siguiente producto: Producto en buenas condiciones, precio justo y entrega rápida."
    },
    {
        "nombre": "resolucion_conflictos",
        "id": "prompt_002",
        "system_prompt": "Eres el supervisor de soporte técnico de una plataforma. Responde si el tipo de problema del cliente es técnico, de servicio o de facturación.",
        "user_prompt": "Cliente (Juan Pérez): Llevo usando su software 45 días y es una basura total, no hace nada de lo que prometieron. ¡Exijo que me devuelvan mi dinero ahora mismo o los voy a denunciar!"
    },
    {
        "nombre": "generacion_codigo_seguro",
        "id": "prompt_003",
        "system_prompt": "Eres un arquitecto de software senior enfocado en ciberseguridad. Clasifica la vulnerabilidad de la solución de software propuesta.Vulnerabilidad critica, alta, media, baja o ninguna vulnerabilidad.",
        "user_prompt": "Escribe una función en Python que reciba un nombre de usuario y consulte una base de datos SQLite para obtener su perfil. Asegúrate de prevenir ataques de Inyección SQL.",
    }
]
for prompt in BANCO_DE_PROMPTS:
    pruebas = 0
    exitos = 0
    fallos = 0
    system_instruction = prompt['system_prompt']
    pregunta = prompt['user_prompt']
    intentos = 3
    for intento in range(intentos):
        pruebas += 1
        try:
            print(f"Intento {intento + 1} de {intentos} para el prompt '{prompt['nombre']}' (ID: {prompt['id']})")
            respuesta = prueba_de_conexion(pregunta, system_instruction)
            print(f"Respuesta obtenida: {respuesta}")
            exitos += 1
        except Exception as e:
            print(f"Error en el intento {intento + 1}: {e}")
            fallos += 1
            if intento == intentos - 1:
                print("Se alcanzó el número máximo de intentos. No se pudo obtener una respuesta.")
print(f"Resumen de pruebas para el banco de prompts con {intentos} intentos por prompt")
print(f"Pruebas: {pruebas}, Éxitos: {exitos}, Fallos: {fallos}")


