"""Orquestador del agente: Groq + openai/gpt-oss-20b + herramientas locales."""
import json
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
from prompts.sistema import SYSTEM_PROMPT
from herramientas.consultas import ranking_peajes, datos_departamentos, normalizar_indicador
from herramientas.analisis import construir_ranking_peajes, comparar_departamentos

client = Groq(api_key=GROQ_API_KEY)

TOOLS = [
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

def ejecutar_herramienta(nombre, args):
    if nombre == "ranking_peajes":
        indicador = normalizar_indicador(args.get("indicador", "veh_total"))
        cantidad = int(args.get("cantidad", 5))
        anio = int(args.get("anio", 2015))
        crudos = ranking_peajes(anio, indicador, cantidad)
        return construir_ranking_peajes(crudos, indicador, cantidad)

    if nombre == "comparar_departamentos":
        indicador = normalizar_indicador(args.get("indicador", "veh_total"))
        anio = int(args.get("anio", 2015))
        deptos = args.get("departamentos", [])
        if isinstance(deptos, str):
            deptos = [d.strip() for d in deptos.split(",")]
        crudos = datos_departamentos(anio, deptos, indicador)
        return comparar_departamentos(crudos, indicador)

    raise ValueError(f"Herramienta desconocida: {nombre}")


def consultar_agente(pregunta: str):
    mensajes = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": pregunta},
    ]
    trazas = []

    # gpt-oss-20b soporta tool use; se usa un bucle secuencial.
    for _ in range(6):
        respuesta = client.chat.completions.create(
            model=LLM_MODEL,
            messages=mensajes,
            tools=TOOLS,
            tool_choice="auto",
            reasoning_effort="medium",
        )
        msg = respuesta.choices[0].message
        mensajes.append(msg)

        if not msg.tool_calls:
            return {"respuesta": msg.content or "", "trazas": trazas}

        for llamada in msg.tool_calls:
            nombre = llamada.function.name
            args = json.loads(llamada.function.arguments or "{}")
            resultado = ejecutar_herramienta(nombre, args)
            trazas.append({"herramienta": nombre, "parametros": args})

            mensajes.append({
                "role": "tool",
                "tool_call_id": llamada.id,
                "content": json.dumps(resultado, ensure_ascii=False, default=str),
            })

    return {
        "respuesta": "Se alcanzó el límite de pasos del agente.",
        "trazas": trazas,
    }
