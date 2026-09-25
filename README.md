# Agente IA para Análisis de Flujo Vehicular

Proyecto guía para estudiantes de Ingeniería Industrial.

## Tecnologías
- Python
- Supabase
- Groq
- `openai/gpt-oss-20b`
- Streamlit
- Pandas
- Plotly

## Preparación

1. Crear entorno virtual:
   `python -m venv .venv`

2. Activar en Windows:
   `.venv\Scripts\activate`

3. Instalar:
   `pip install -r requirements.txt`

4. Copiar `.env.example` como `.env` y completar claves.

5. Probar:
   `pytest -q`

6. Ejecutar:
   `streamlit run app.py`

## Secuencia SDD
Leer `specs/requirements.md`, luego `specs/spec.md` y finalmente `specs/tasks.md`.

## Actividad sugerida
Probar:
- ¿Cuáles fueron los 5 peajes con mayor flujo en 2025?
- Compara Lima e Ica en 2025.
- ¿Por qué existe congestión en el peaje con mayor flujo?

La tercera pregunta permite evaluar si el agente evita afirmar causalidad sin variables suficientes.
