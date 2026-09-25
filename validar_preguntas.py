"""Script para validar al menos 6 preguntas reales del usuario (Paso 10 de SPED)."""
import sys
import os
import json
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from agente import consultar_agente

PREGUNTAS = [
    {
        "id": 1,
        "categoria": "Ranking Flujo Total",
        "pregunta": "¿Cuáles fueron los 5 peajes con mayor flujo vehicular total en 2015?"
    },
    {
        "id": 2,
        "categoria": "Ranking Vehículos Pesados",
        "pregunta": "¿Cuáles fueron los 3 peajes con mayor tráfico de vehículos pesados en 2015?"
    },
    {
        "id": 3,
        "categoria": "Comparación Bivariada Departamentos",
        "pregunta": "¿Cómo se compara el flujo vehicular total entre Lima e Ica en 2015?"
    },
    {
        "id": 4,
        "categoria": "Comparación Multidepartamental",
        "pregunta": "¿Qué departamento tuvo mayor flujo vehicular entre Arequipa, Cusco y Puno en 2014?"
    },
    {
        "id": 5,
        "categoria": "Ranking Vehículos Ligeros",
        "pregunta": "¿Cuál fue el peaje con mayor cantidad de vehículos ligeros en 2015?"
    },
    {
        "id": 6,
        "categoria": "Análisis Contextual de Periodos",
        "pregunta": "¿Cuáles fueron los 5 principales peajes por flujo en 2026 y qué advertencia temporal aplica?"
    }
]

def ejecutar_validacion():
    print("=" * 70)
    print("EJECUTANDO PASO 10: VALIDACIÓN DE 6 PREGUNTAS REALES")
    print("=" * 70)
    
    resultados = []
    os.makedirs("output/reportes", exist_ok=True)

    for item in PREGUNTAS:
        pid = item["id"]
        cat = item["categoria"]
        preg = item["pregunta"]
        
        print(f"\n[{pid}/6] Pregunta ({cat}):")
        print(f"    '{preg}'")
        
        inicio = time.time()
        res = consultar_agente(preg)
        duracion = round(time.time() - inicio, 2)
        
        registro = {
            "id": pid,
            "categoria": cat,
            "pregunta": preg,
            "duracion_segundos": duracion,
            "trazas": res.get("trazas", []),
            "respuesta": res.get("respuesta", "")
        }
        resultados.append(registro)
        
        print(f" -> Tiempo: {duracion}s | Herramientas invocadas: {[t['herramienta'] for t in res.get('trazas', [])]}")
        print(f" -> Respuesta:\n{res.get('respuesta', '')}\n")
        print("-" * 70)

    # Guardar en formato JSON
    json_path = "output/reportes/evidencia_6_preguntas.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Resultados exportados a {json_path}")

    # Guardar en formato Markdown
    md_path = "output/reportes/evidencia_6_preguntas.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Evidencia de Validación de 6 Preguntas Reales (Paso 10 SPED)\n\n")
        f.write("Validación del agente con **Groq (`openai/gpt-oss-20b`)** y **Supabase**.\n\n")
        for r in resultados:
            f.write(f"## Pregunta {r['id']}: {r['categoria']}\n\n")
            f.write(f"**Consulta:** `{r['pregunta']}`  \n")
            f.write(f"**Tiempo de respuesta:** {r['duracion_segundos']} s  \n")
            f.write(f"**Herramientas ejecutadas:** `{json.dumps(r['trazas'], ensure_ascii=False)}`\n\n")
            f.write(f"### Respuesta generada por el agente:\n\n{r['respuesta']}\n\n")
            f.write("---\n\n")
    print(f"✅ Evidencia en Markdown exportada a {md_path}")

if __name__ == "__main__":
    ejecutar_validacion()
