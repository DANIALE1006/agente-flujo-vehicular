# Guía de Publicación en Streamlit Community Cloud (Acceso Público)

Esta guía explica paso a paso cómo publicar tu **Agente de Análisis de Flujo Vehicular** en **Streamlit Community Cloud** de forma 100% gratuita y pública.

---

## 📋 Preparativos Realizados en el Código

El proyecto ya fue acondicionado y probado para funcionar de inmediato en la nube:
1. **`config.py` actualizado:** Detecta automáticamente las credenciales tanto de tu archivo `.env` local como de los `Secrets` seguros de Streamlit Cloud.
2. **`.gitignore` reforzado:** Protege `.env` y `.streamlit/secrets.toml` para que tus claves privadas de Supabase y Groq **nunca** se hagan públicas en GitHub.
3. **`requirements.txt` validado:** Contiene todas las dependencias necesarias (`streamlit`, `supabase`, `groq`, `python-dotenv`, `pandas`, `plotly`, `pytest`).
4. **`.streamlit/config.toml` creado:** Define el tema visual y optimiza la configuración del servidor web.
5. **`.streamlit/secrets.toml.example` listo:** Contiene el formato exacto para copiar y pegar en Streamlit Cloud.

---

## 🚀 Paso 1: Subir el Proyecto a GitHub

Streamlit Cloud se conecta a un repositorio de GitHub para compilar y desplegar la app.

### Opción A: Desde la Web de GitHub (Más rápida, sin instalar nada)
1. Inicia sesión en [GitHub.com](https://github.com).
2. Haz clic en el botón verde **"New"** o visita [github.com/new](https://github.com/new).
3. Nombra tu repositorio: por ejemplo `agente-flujo-vehicular`.
4. Elige si prefieres que sea **Public** (Público) o **Private** (Privado) — *ambos funcionan con Streamlit Cloud*.
5. Deja desmarcadas las opciones de "Add README" o ".gitignore" (ya los tenemos creados). Haz clic en **"Create repository"**.
6. En la pantalla siguiente, haz clic en el enlace que dice **"uploading an existing file"** (subir archivos existentes).
7. Arrastra todos los archivos y carpetas de esta carpeta:
   - `app.py`
   - `config.py`
   - `agente.py`
   - `requirements.txt`
   - `README.md`
   - Carpetas: `herramientas/`, `servicios/`, `prompts/`, `specs/`, `tests/`, `.streamlit/`
   > ⚠️ **IMPORTANTE:** NO subas el archivo `.env` (las contraseñas se configuran en el Paso 3).
8. Haz clic en **"Commit changes"**.

### Opción B: Con GitHub Desktop
1. Si tienes instalado [GitHub Desktop](https://desktop.github.com/):
2. Menú **File** > **Add Local Repository...** > Selecciona la carpeta del proyecto.
3. Haz clic en **Publish repository** hacia tu cuenta de GitHub.

---

## 🌐 Paso 2: Conectar y Desplegar en Streamlit Cloud

1. Entra a [share.streamlit.io](https://share.streamlit.io).
2. Inicia sesión haciendo clic en **"Continue with GitHub"**.
3. Haz clic en el botón azul **"Create app"** (o "New app").
4. Completa los campos del formulario:
   - **Repository:** Selecciona `tu-usuario/agente-flujo-vehicular`
   - **Branch:** `main` (o `master`)
   - **Main file path:** `app.py`
   - **App URL (opcional):** Puedes personalizar el subdominio (ej: `agente-flujo-vehicular.streamlit.app`).

---

## 🔐 Paso 3: Configurar los Secrets (Credenciales Seguras)

Antes de hacer clic en Deploy, debes ingresar las credenciales de Supabase y Groq:

1. En la parte inferior del formulario de despliegue, haz clic en **"Advanced settings..."**.
2. En el panel que se abre, selecciona la pestaña **"Secrets"**.
3. Pega exactamente el siguiente bloque de configuración:

```toml
SUPABASE_URL = "https://kyuucnxdbqfbkrlbpczj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5dXVjbnhkYnFmYmtybGJwY3pqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAwMjMxMTUsImV4cCI6MjEwNTU5OTExNX0.2OUjDUF5Co6sd9q_uKeQQDySd5iJMr2rmM2qjgJE6wo"
GROQ_API_KEY = "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"
LLM_MODEL = "openai/gpt-oss-20b"
```

4. Haz clic en **"Save"**.

---

## 🎉 Paso 4: Lanzamiento

1. Haz clic en el botón azul **"Deploy!"**.
2. Streamlit Cloud clonará tu repositorio, instalará las librerías de `requirements.txt` y pondrá en marcha la aplicación.
3. En aproximadamente 1 a 2 minutos, tu aplicación estará **en línea y pública** con una URL accesible desde cualquier navegador o celular (por ejemplo: `https://tu-app.streamlit.app`).
