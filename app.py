import streamlit as st
import pandas as pd
from utils.ui import inject_css, hero, kpi, sidebar_header, card_buttons

# ==============================
# Configuración inicial de la app
# ==============================
st.set_page_config(
    page_title="Smart Housing Madrid",
    layout="wide",
    page_icon="🧭"
)

# ==============================
# Mostrar logos en la cabecera del menú lateral
# ==============================
sidebar_header()

# ==============================
# Inyecta estilos personalizados
# ==============================
inject_css()

# ==============================
# Renderiza el encabezado principal (hero con skyline)
# ==============================
hero()


# ==============================
# Nueva sección de tarjetas tipo botón (visual más moderno)
# ==============================
st.markdown("## Conoce el mercado ⬇️")

# valores del DataFrame
precio_ciudad = "4.120"
distrito_caro = "Centro"
distrito_barato = "Puente de Vallecas"
variacion = "3.2%"

# <- renderiza las cuatro tarjetas alineadas
card_buttons(precio_ciudad, distrito_caro, distrito_barato, variacion)

# ==============================
# Opciones principales: botones grandes de navegación
# ==============================
st.subheader("¿Qué quieres hacer hoy?")

# Primera fila de botones
row1 = st.columns(2)
with row1[0]:
    if st.button("🏠 Comprar:  Encuentra tu hogar", key="buy", use_container_width=True):
        st.session_state["objetivo"] = "comprar"
        st.switch_page("pages/1_Asistente.py")

with row1[1]:
    if st.button("📈 Vender:  Valora tu propiedad", key="sell", use_container_width=True):
        st.session_state["objetivo"] = "vender"
        st.switch_page("pages/1_Asistente.py")

# Segunda fila de botones
row2 = st.columns(2)
with row2[0]:
    if st.button("🗺️ Explorar:  Descubre zonas", key="explore", use_container_width=True):
        st.session_state["objetivo"] = "explorar"
        st.switch_page("pages/1_Asistente.py")

with row2[1]:
    if st.button("🔬 Modo avanzado: Análisis profundo", key="advanced_views", use_container_width=True):
        st.session_state["objetivo"] = "avanzadas"
        st.switch_page("pages/6_Vistas_Avanzadas.py")

# ==============================
# Pie de página (créditos académicos del TFM)
# ==============================
st.caption(
    """
    <div style="text-align: center;">
        TFM: Modelado del precio de la vivienda en Madrid: enfoque multidimensional basado en técnicas de Big Data y Machine Learning (2015–2024).
        <br><br>
        Máster Data Science, Big Data & Business Analytics 2024-2025.
        <br><br>
        UCM.
    </div>
    """,
    unsafe_allow_html=True
)
