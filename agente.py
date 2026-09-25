"""Orquestador del agente: Groq + openai/gpt-oss-20b + herramientas locales."""
import os
import json
from groq import Groq
import config
from prompts.sistema import SYSTEM_PROMPT
from herramientas.consultas import ranking_peajes, datos_departamentos, normalizar_indicador
from herramientas.analisis import construir_ranking_peajes, comparar_departamentos

def get_groq_client():
    api_key = config.GROQ_API_KEY or config._get_config_value("GROQ_API_KEY")
    return Groq(api_key=api_key)

BASE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ranking_peajes",
            "description": "Obtiene el ranking de peajes para un año e indicador.",
            "parameters": {
                "type": "object",
                "properties": {
                    "anio": {"type": "integer"},
                    "indicador": {
                        "type": "string",
                        "enum": ["veh_total", "veh_imd", "veh_ligeros_total", "veh_pesados_total"]
                    },
                    "cantidad": {"type": "integer", "minimum": 1, "maximum": 20}
                },
                "required": ["anio"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "comparar_departamentos",
            "description": "Compara el valor agregado de un indicador entre departamentos en un año.",
            "parameters": {
                "type": "object",
                "properties": {
                    "anio": {"type": "integer"},
                    "departamentos": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2
                    },
                    "indicador": {
                        "type": "string",
                        "enum": ["veh_total", "veh_imd", "veh_ligeros_total", "veh_pesados_total"]
                    }
                },
                "required": ["anio", "departamentos"]
            }
        }
    }
]

# Registrar aliases para proteger contra tokens de canal (<|channel|>commentary) en Groq
TOOLS = list(BASE_TOOLS)
for t in BASE_TOOLS:
    for suffix in ["<|channel|>commentary", "<|channel|>thought"]:
        TOOLS.append({
            "type": "function",
            "function": {
                "name": f"{t['function']['name']}{suffix}",
                "description": t["function"]["description"],
                "parameters": t["function"]["parameters"]
            }
        })

def ejecutar_herramienta(nombre, args):
    # Limpiar cualquier sufijo de canal como <|channel|>commentary
    nombre_limpio = str(nombre).split("<|")[0].strip()

    if nombre_limpio == "ranking_peajes":
        indicador = normalizar_indicador(args.get("indicador", "veh_total"))
        cantidad = int(args.get("cantidad", 5))
        anio = int(args.get("anio", 2015))
        crudos = ranking_peajes(anio, indicador, cantidad)
        return construir_ranking_peajes(crudos, indicador, cantidad)

    if nombre_limpio == "comparar_departamentos":
        indicador = normalizar_indicador(args.get("indicador", "veh_total"))
        anio = int(args.get("anio", 2015))
        deptos = args.get("departamentos", [])
        if isinstance(deptos, str):
            deptos = [d.strip() for d in deptos.split(",")]
        crudos = datos_departamentos(anio, deptos, indicador)
        return comparar_departamentos(crudos, indicador)

    raise ValueError(f"Herramienta desconocida: {nombre}")


def consultar_agente(pregunta: str):
    client = get_groq_client()
    modelo = config.LLM_MODEL or config._get_config_value("LLM_MODEL", "openai/gpt-oss-20b")

    mensajes = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": pregunta},
    ]
    trazas = []

    for _ in range(6):
        intentos = 0
        respuesta = None
        while intentos < 2:
            try:
                respuesta = client.chat.completions.create(
                    model=modelo,
                    messages=mensajes,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.0,
                )
                break
            except Exception as e:
                intentos += 1
                if intentos >= 2:
                    raise e

        msg = respuesta.choices[0].message
        mensajes.append(msg)

        if not msg.tool_calls:
            return {"respuesta": msg.content or "", "trazas": trazas}

        for llamada in msg.tool_calls:
            nombre = llamada.function.name
            args = json.loads(llamada.function.arguments or "{}")
            resultado = ejecutar_herramienta(nombre, args)

            nombre_visible = str(nombre).split("<|")[0].strip()
            trazas.append({"herramienta": nombre_visible, "parametros": args})

            mensajes.append({
                "role": "tool",
                "tool_call_id": llamada.id,
                "content": json.dumps(resultado, ensure_ascii=False, default=str),
            })

    return {
        "respuesta": "Se alcanzó el límite de pasos del agente.",
        "trazas": trazas,
    }

