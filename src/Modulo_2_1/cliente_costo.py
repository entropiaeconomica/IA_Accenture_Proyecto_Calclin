

COSTO_POR_1000_TOKENS = 0.002  # valor de referencia, puede ajustarse según el costo real de la API

costo_total_sesion = 0

def registrar_costo(respuesta: dict) -> float:
	global costo_total_sesion
	metadatos = respuesta.get("usageMetadata", {})
	total_tokens = metadatos.get("totalTokenCount", 0)
	costo_estimado_consulta = (total_tokens / 1000) * COSTO_POR_1000_TOKENS
	costo_total_sesion = costo_total_sesion + costo_estimado_consulta
	print(f"Operación: {total_tokens} tokens, costo estimado: ${costo_estimado_consulta:.5f} (acumulado: ${costo_total_sesion:.5f})")
	return costo_estimado_consulta