import streamlit as st
import pandas as pd
from utils.ui import inject_css, hero, kpi

# Configuración inicial de la app
st.set_page_config(
    page_title="Smart Housing Madrid",
    layout="wide",
    page_icon="🧭"
)

# Inyecta estilos personalizados
inject_css()

# Renderiza el encabezado principal
hero()

# KPIs iniciales
st.write("")
c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi("€/m² (ciudad)", "4.120", delta=2.4)
with c2:
    kpi("Distrito más caro", "Centro")
with c3:
    kpi("Distrito más barato", "Puente de Vallecas")
with c4:
    kpi("Variación anual", "3.2%")

st.markdown("---")
st.subheader("¿Qué quieres hacer hoy?")

# Opciones principales: botones grandes en dos filas
row1 = st.columns(2)
with row1[0]:
    if st.button("🏠 Comprar\nEncuentra tu hogar", key="buy", use_container_width=True):
        st.session_state["objetivo"] = "comprar"
        st.switch_page("pages/1_Flujo_Usuario.py")
with row1[1]:
    if st.button("📈 Vender\nValora tu propiedad", key="sell", use_container_width=True):
        st.session_state["objetivo"] = "vender"
        st.switch_page("pages/1_Flujo_Usuario.py")

row2 = st.columns(2)
with row2[0]:
    if st.button("🗺️ Explorar barrios\nDescubre zonas", key="explore", use_container_width=True):
        st.session_state["objetivo"] = "explorar"
        st.switch_page("pages/1_Flujo_Usuario.py")
with row2[1]:
    if st.button("🔬 Vistas avanzadas\nAnálisis profundo", key="advanced_views", use_container_width=True):
        st.session_state["objetivo"] = "avanzadas"
        st.switch_page("pages/6_Vistas_Avanzadas.py")

st.caption("Encuentra el mejor lugar, en el mejor momento.")
