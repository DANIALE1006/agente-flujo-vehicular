import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import GROQ_API_KEY, LLM_MODEL
from groq import Groq
from agente import consultar_agente

def test_groq_conexion():
    print("\n--- PROBANDO PASO 7: CONEXIÓN A GROQ ---")
    client = Groq(api_key=GROQ_API_KEY)
    respuesta = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": "Hola, responde OK"}],
    )
    contenido = respuesta.choices[0].message.content
    assert contenido is not None and len(contenido) > 0
    print(f"✅ Conexión con Groq ({LLM_MODEL}) exitosa. Respuesta: {contenido.strip()}")

def test_agente_tool_calling_ranking():
    print("\n--- PROBANDO PASO 8: TOOL CALLING CON AGENTE (RANKING) ---")
    pregunta = "¿Cuáles son los 3 peajes con mayor flujo de vehículos pesados en 2015?"
    resultado = consultar_agente(pregunta)
    
    assert "respuesta" in resultado and len(resultado["respuesta"]) > 0
    assert len(resultado["trazas"]) > 0, "El agente debió llamar a al menos una herramienta"
    
    herramientas_usadas = [t["herramienta"] for t in resultado["trazas"]]
    assert "ranking_peajes" in herramientas_usadas
    print(f"✅ Tool calling exitoso. Herramientas usadas: {herramientas_usadas}")
    print(f"Respuesta resumida: {resultado['respuesta'][:200]}...")

def test_agente_tool_calling_comparacion():
    print("\n--- PROBANDO PASO 8: TOOL CALLING CON AGENTE (COMPARACIÓN) ---")
    pregunta = "¿Cómo se compara el flujo vehicular entre Lima e Ica en 2015?"
    resultado = consultar_agente(pregunta)
    
    assert "respuesta" in resultado and len(resultado["respuesta"]) > 0
    assert len(resultado["trazas"]) > 0, "El agente debió llamar a al menos una herramienta"
    
    herramientas_usadas = [t["herramienta"] for t in resultado["trazas"]]
    assert "comparar_departamentos" in herramientas_usadas
    print(f"✅ Tool calling de comparación exitoso. Herramientas usadas: {herramientas_usadas}")
    print(f"Respuesta resumida: {resultado['respuesta'][:200]}...")

if __name__ == "__main__":
    test_groq_conexion()
    test_agente_tool_calling_ranking()
    test_agente_tool_calling_comparacion()
