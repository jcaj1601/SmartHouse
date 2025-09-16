import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from utils.ui import inject_css

# ==============================
# Configuración inicial
# ==============================
st.set_page_config(page_title="Calculadora", layout="wide", page_icon="🧭")
inject_css()
st.title("🧮 Calculadora de precio")

# ==============================
# Lista de distritos demo
# ==============================
DIST_LIST = [
    "Centro","Arganzuela","Retiro","Salamanca","Chamartín","Tetuán","Chamberí",
    "Fuencarral-El Pardo","Moncloa-Aravaca","Latina","Carabanchel","Usera",
    "Puente de Vallecas","Moratalaz","Ciudad Lineal","Hortaleza","Villaverde",
    "Villa de Vallecas","Vicálvaro","San Blas-Canillejas","Barajas"
]

# ==============================
# Prefill desde Asistente (si existe)
# ==============================
default_distrito = st.session_state.get("selected_distrito", "Centro")
default_superficie = st.session_state.get("calc_superficie", 85)
default_antiguedad = st.session_state.get("calc_antiguedad", 35)
default_ascensor = st.session_state.get("calc_ascensor", 1)  # 1=Sí, 0=No

# ==============================
# Inputs
# ==============================
c1, c2, c3 = st.columns(3)
with c1:
    distrito = st.selectbox("Distrito", DIST_LIST, index=DIST_LIST.index(default_distrito))
    superficie = st.number_input("Superficie (m²)", 20, 400, int(default_superficie))
with c2:
    habitaciones = st.selectbox("Habitaciones", [1,2,3,4], index=1)
    ascensor = st.selectbox("Ascensor", ["Sí","No"], index=0 if default_ascensor==1 else 1)
with c3:
    cerca_metro = st.selectbox("Cercanía a Metro", ["Sí","No"], index=0)
    antiguedad = st.slider("Antigüedad (años)", 0, 120, int(default_antiguedad))

# ==============================
# Botón de cálculo (modo demo)
# ==============================
if st.button("Calcular Intervalos de Confianza", use_container_width=True):
    # --- DEMO: Generamos valores ficticios ---
    base = 4000 + np.random.randint(-500, 500)   # precio base €/m²
    y50 = base
    y10 = base - np.random.randint(300, 600)
    y90 = base + np.random.randint(300, 600)

    st.success(f"Mediana: **{y50:,.0f} €/m²** · Intervalo **[{y10:,.0f} – {y90:,.0f}] €/m²**")

    # --- Demo con gráfica tipo bullet ---
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge+delta",
        value=y50,
        number={'suffix':" €/m²"},
        delta={'reference': y10, 'increasing': {'color': '#3FA34D'}, 'decreasing': {'color': '#AA1927'}},
        gauge={'shape': "bullet",
               'axis': {'range': [max(0,y10*0.8), y90*1.2]},
               'bar': {'color':'#1B3B6F'},
               'threshold': {'line': {'color': "#AA1927", 'width': 3}, 'thickness': 0.75, 'value': y90}},
        domain={'x':[0,1],'y':[0,1]}
    ))
    fig.update_layout(height=140, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

    # --- Demo: importancia ficticia de variables ---
    st.markdown("---")
    st.subheader("¿Qué variables pesan más en esta predicción?")
    features = ["Superficie", "Distrito", "Antigüedad", "Ascensor", "Cercanía a Metro"]
    vals = np.random.rand(len(features))
    vals = vals / vals.sum()  # normalizar
    fig_imp = px.bar(x=vals[::-1], y=features[::-1], orientation="h",
                     title="Impacto relativo de variables")
    st.plotly_chart(fig_imp, use_container_width=True)

# ==============================
# Botón de regreso al Asistente
# ==============================
if st.button("⬅️ Volver al Asistente", use_container_width=True):
    st.switch_page("pages/1_Asistente.py")
