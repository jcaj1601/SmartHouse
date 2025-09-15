
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui import inject_css

st.set_page_config(page_title="Comparador", layout="wide", page_icon="🧭")
inject_css()
st.title("Comparador de distritos — Demo")

try:
    df = pd.read_csv("data/distritos_madrid_coords.csv")
except Exception:
    df = pd.DataFrame({
        "distrito":["Chamartín","Hortaleza","Puente de Vallecas","Arganzuela","Centro","Tetuán"],
        "precio_m2":[4650,3970,2120,4300,5200,3600],
        "variacion_interanual":[5.2,1.8,-0.5,3.1,4.7,0.9]
    })

sel = st.multiselect("Selecciona distritos", df["distrito"].tolist(), default=df["distrito"].tolist()[:3])
dff = df[df["distrito"].isin(sel)]

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(dff, x="distrito", y="precio_m2", title="€/m² por distrito")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(dff, x="distrito", y="variacion_interanual", title="Variación interanual (%)")
    st.plotly_chart(fig, use_container_width=True)

st.download_button("📥 Descargar comparativa (CSV)", data=dff.to_csv(index=False).encode(), file_name="comparador_distritos.csv")
