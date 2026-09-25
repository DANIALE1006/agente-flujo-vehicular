"""Interfaz Streamlit del agente de flujo vehicular."""
import streamlit as st
import pandas as pd
from agente import consultar_agente, ejecutar_herramienta
from herramientas.graficos import grafico_ranking

st.set_page_config(
    page_title="Agente IA - Flujo Vehicular (SPED)",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 Agente IA para Análisis de Flujo Vehicular")
st.caption("Implementado bajo metodología SPED con Groq (`openai/gpt-oss-20b`), Python y Supabase")

# Barra lateral con información y consultas sugeridas
with st.sidebar:
    st.header("⚙️ Configuración y Estado")
    st.success("✅ Base de Datos: Supabase conectada")
    st.success("✅ LLM: Groq `openai/gpt-oss-20b`")
    st.info("📊 Tabla de datos: `flujo_vehicular` (11,532 registros)")
    
    st.subheader("💡 Consultas de Ejemplo")
    ejemplos = [
        "¿Cuáles fueron los 5 peajes con mayor flujo vehicular total en 2015?",
        "¿Cuáles fueron los 3 peajes con mayor tráfico de vehículos pesados en 2015?",
        "¿Cómo se compara el flujo vehicular total entre Lima e Ica en 2015?",
        "¿Qué departamento tuvo mayor flujo vehicular entre Arequipa, Cusco y Puno en 2014?",
        "¿Cuál fue el peaje con mayor cantidad de vehículos ligeros en 2015?",
        "¿Cuáles son los 5 principales peajes por flujo en 2026 y qué advertencia temporal aplica?"
    ]
    
    consulta_seleccionada = None
    for ej in ejemplos:
        if st.button(ej, use_container_width=True):
            st.session_state["consulta_actual"] = ej

if "consulta_actual" not in st.session_state:
    st.session_state["consulta_actual"] = "¿Cuáles fueron los 5 peajes con mayor flujo vehicular total en 2015?"

pregunta = st.text_area(
    "Escriba su consulta en lenguaje natural:",
    value=st.session_state.get("consulta_actual", ""),
    height=100
)

col1, col2 = st.columns([1, 5])
with col1:
    ejecutar = st.button("🚀 Analizar", type="primary", use_container_width=True)

if ejecutar and pregunta.strip():
    with st.spinner("🤖 El agente está razonando y consultando Supabase..."):
        try:
            resultado = consultar_agente(pregunta)
            
            st.markdown("### 📋 Respuesta del Agente")
            st.markdown(resultado["respuesta"])

            trazas = resultado.get("trazas", [])
            
            # Si se utilizó alguna herramienta, mostrar visualización si aplica
            if trazas:
                st.markdown("---")
                st.markdown("### 📊 Gráficos y Visualización de Datos")
                for traza in trazas:
                    h_nombre = traza.get("herramienta")
                    params = traza.get("parametros", {})
                    
                    if h_nombre == "ranking_peajes":
                        datos_ranking = ejecutar_herramienta(h_nombre, params)
                        if datos_ranking:
                            ind = params.get("indicador", "veh_total")
                            fig = grafico_ranking(datos_ranking, indicador=ind)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                                
                    elif h_nombre == "comparar_departamentos":
                        datos_comp = ejecutar_herramienta(h_nombre, params)
                        if datos_comp:
                            df_comp = pd.DataFrame(datos_comp)
                            ind = params.get("indicador", "veh_total")
                            st.bar_chart(data=df_comp, x="departamento", y=ind)

            with st.expander("🔍 Trazabilidad y Llamadas a Herramientas (SPED)"):
                st.write("Herramientas y parámetros ejecutados de forma determinística:")
                st.json(trazas)
                
        except Exception as e:
            st.error(f"❌ Ocurrió un error al procesar la consulta: {e}")

