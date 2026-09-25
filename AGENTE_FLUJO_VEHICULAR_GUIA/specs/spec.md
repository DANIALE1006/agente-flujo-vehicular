# SPECIFICATION

## Arquitectura
Usuario → Streamlit → Agente (Groq / openai/gpt-oss-20b) → Herramientas Python → Supabase → Resultado → Agente → Usuario.

## Responsabilidades
- LLM: comprender, seleccionar herramienta e interpretar.
- Python: consultar, calcular y visualizar.
- Supabase: fuente de verdad.
- Streamlit: interfaz.

## Herramientas V1
1. ranking_peajes
2. comparar_departamentos

## Criterio de aceptación
Una consulta debe producir resultados numéricos verificables contra Supabase y registrar qué herramienta y parámetros fueron usados.
