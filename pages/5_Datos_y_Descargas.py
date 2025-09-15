
import streamlit as st
import pandas as pd
from utils.ui import inject_css

st.set_page_config(page_title="Datos y descargas", layout="wide", page_icon="🧭")
inject_css()
st.title("Datos y descargas")

st.write("Activos disponibles:")
st.write("- vivienda_imputada.xlsx")
st.write("- Barrios.json / Distritos.json")
st.write("- catalogo_distritos_barrios.csv")

try:
    df = pd.read_excel("data/vivienda_imputada.xlsx")
    st.dataframe(df.head(50), use_container_width=True)
except Exception as e:
    st.warning(f"No se pudo cargar vivienda_imputada.xlsx: {e}")

st.caption("Integra aquí tus datasets completos y normaliza nombres de columnas si es necesario.")
