"""Configuración central del proyecto."""
import os
from dotenv import load_dotenv

load_dotenv()

def _get_config_value(key: str, default: str = "") -> str:
    """Obtiene una variable desde variables de entorno (.env) o desde st.secrets de Streamlit Cloud."""
    val = os.getenv(key)
    if not val:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and key in st.secrets:
                val = str(st.secrets[key])
        except Exception:
            pass
    return val or default

SUPABASE_URL = _get_config_value("SUPABASE_URL", "")
SUPABASE_KEY = _get_config_value("SUPABASE_KEY", "")
GROQ_API_KEY = _get_config_value("GROQ_API_KEY", "")
LLM_MODEL = _get_config_value("LLM_MODEL", "openai/gpt-oss-20b")
TABLE_NAME = "flujo_vehicular"

def validar_configuracion():
    faltantes = [
        nombre for nombre, valor in {
            "SUPABASE_URL": SUPABASE_URL,
            "SUPABASE_KEY": SUPABASE_KEY,
            "GROQ_API_KEY": GROQ_API_KEY,
        }.items() if not valor
    ]
    if faltantes:
        raise RuntimeError("Faltan variables de configuración (en .env o Streamlit Secrets): " + ", ".join(faltantes))

