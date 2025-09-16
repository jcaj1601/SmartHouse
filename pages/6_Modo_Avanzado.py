import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui import inject_css


st.set_page_config(page_title="Vistas avanzadas", layout="wide", page_icon="🧭")
inject_css()
st.title("Vistas avanzadas — Análisis profundo")

# Attempt to load the default dataset of districts. If not found, fall back to
# a small demo DataFrame. This ensures the page remains functional even if the
# user hasn't provided the CSV.
try:
    df = pd.read_csv("data/distritos_madrid_coords.csv")
except Exception:
    df = pd.DataFrame({
        "distrito": ["Chamartín", "Hortaleza", "Puente de Vallecas", "Arganzuela", "Centro", "Tetuán"],
        "precio_m2": [4650, 3970, 2120, 4300, 5200, 3600],
        "variacion_interanual": [5.2, 1.8, -0.5, 3.1, 4.7, 0.9],
        "lat": [40.449, 40.478, 40.387, 40.399, 40.418, 40.458],
        "lon": [-3.677, -3.642, -3.659, -3.700, -3.703, -3.703]
    })

# Only attempt advanced analytics if numeric columns exist
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(num_cols) >= 2:
    corr = df[num_cols].corr()
    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=num_cols,
        y=num_cols,
        colorscale='Blues',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlación")
    ))
    heatmap.update_layout(title="Matriz de correlación", xaxis_title="", yaxis_title="")
    st.plotly_chart(heatmap, use_container_width=True)

# Scatter plot between €/m² and variación interanual
if "precio_m2" in df.columns and "variacion_interanual" in df.columns:
    fig_scatter = px.scatter(
        df,
        x="precio_m2",
        y="variacion_interanual",
        text="distrito" if "distrito" in df.columns else None,
        title="Relación €/m² vs variación interanual",
        labels={"precio_m2": "€/m²", "variacion_interanual": "Variación (%)"},
        color_discrete_sequence=["#0B3D91"]
    )
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Estadísticas descriptivas")
st.dataframe(df.describe().transpose(), use_container_width=True)

# Provide a download of the underlying data for further offline analysis
st.download_button(
    "📥 Descargar datos (CSV)",
    data=df.to_csv(index=False).encode(),
    file_name="distritos_avanzado.csv",
    help="Descarga el dataset utilizado en este análisis.",
    use_container_width=True
)