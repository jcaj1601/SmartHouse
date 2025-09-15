
import streamlit as st
import numpy as np
import plotly.express as px
from utils.ui import inject_css

st.set_page_config(page_title="Importancia", layout="wide", page_icon="🧭")
inject_css()
st.title("Importancia global — Demo")
features = ["Renta distrital","Cercanía a Metro","Zonas verdes","Paro","Turismo (Airbnb)","Ruido"]
vals = np.array([0.28,0.22,0.16,0.14,0.12,0.08])
fig = px.bar(x=vals, y=features, orientation="h", title="Importancia global (demo)")
st.plotly_chart(fig, use_container_width=True)
st.info("Sustituye por resultados reales de SHAP global / FI del modelo.")
