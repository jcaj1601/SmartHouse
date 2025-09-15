
import streamlit as st
import pandas as pd
from utils.ui import inject_css, hero, kpi

st.set_page_config(page_title="SmartHousing Madrid", layout="wide", page_icon="🧭")
inject_css()
hero()

st.write("")
c1, c2, c3, c4 = st.columns(4)
with c1: kpi("€/m² (ciudad)", "4.120", delta=2.4)
with c2: kpi("Distrito más caro", "Centro")
with c3: kpi("Distrito más barato", "Puente de Vallecas")
with c4: kpi("Variación anual", "3.2%")

st.markdown("---")
st.subheader("¿Qué quieres hacer hoy?")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Comprar", use_container_width=True):
        st.session_state["objetivo"]="comprar"
        st.switch_page("pages/1_Flujo_Usuario.py")
with col2:
    if st.button("📈 Vender", use_container_width=True):
        st.session_state["objetivo"]="vender"
        st.switch_page("pages/1_Flujo_Usuario.py")
with col3:
    if st.button("🗺️ Explorar barrios", use_container_width=True):
        st.session_state["objetivo"]="explorar"
        st.switch_page("pages/1_Flujo_Usuario.py")

st.caption("Demo visual: sustituye métricas por tus datos agregados 2015–2024.")
