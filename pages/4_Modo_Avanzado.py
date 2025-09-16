import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui import inject_css

# ==============================
# Configuración inicial
# ==============================
st.set_page_config(page_title="Análisis avanzado", layout="wide", page_icon="🧭")
inject_css()
st.title("")
st.title("🔬 Análisis avanzado del mercado")

# ==============================
# Dataset demo
# ==============================
df = pd.DataFrame({
    "distrito": [
        "Chamartín","Hortaleza","Puente de Vallecas",
        "Arganzuela","Centro","Tetuán","Carabanchel","Usera","Latina"
    ],
    "precio_m2": [4650, 3970, 2120, 4300, 5200, 3600, 2950, 2700, 3100],
    "variacion_interanual": [5.2, 1.8, -0.5, 3.1, 4.7, 0.9, 1.2, -0.8, 0.5],
    "renta": [25000, 23000, 18000, 24000, 28000, 20000, 19000, 17000, 18500],
    "paro": [8.2, 9.1, 14.5, 10.2, 7.5, 11.8, 12.3, 15.0, 13.7]
})
st.caption("🗂️ Dataset ")

# ==============================
# Tabs de análisis
# ==============================
tab1, tab2, tab3 = st.tabs([
    "📊 Correlaciones", 
    "⭐ Importancia de variables", 
    "📥 Descarga de datos"
])

# --- TAB 1: Correlaciones ---
with tab1:
    st.subheader("Matriz de correlaciones")

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr = df[num_cols].corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values, x=num_cols, y=num_cols,
        colorscale='Blues', zmin=-1, zmax=1,
        colorbar=dict(title="Correlación")
    ))
    heatmap.update_layout(title="Matriz de correlación")
    st.plotly_chart(heatmap, use_container_width=True)

    st.subheader("Scatter €/m² vs variación interanual")
    fig_scatter = px.scatter(
        df, x="precio_m2", y="variacion_interanual",
        text="distrito",
        title="Relación €/m² vs variación (%)",
        labels={"precio_m2": "€/m²", "variacion_interanual": "Variación (%)"},
        color="variacion_interanual", color_continuous_scale="RdYlGn"
    )
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 2: Importancia ---
with tab2:
    st.subheader("Importancia global de variables")

    features = ["Renta distrital","Cercanía a Metro","Zonas verdes","Paro","Turismo (Airbnb)","Ruido"]
    vals = np.array([0.28, 0.22, 0.16, 0.14, 0.12, 0.08])

    fig = px.bar(
        x=vals[::-1], y=features[::-1],
        orientation="h", title="Importancia global"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("👉 Sustituir con resultados reales de SHAP o Feature Importance del modelo.")

# --- TAB 3: Descargas ---
with tab3:
    st.subheader("Datasets disponibles")

    st.write("Archivos de ejemplo:")
    st.write("- vivienda_imputada.xlsx")
    st.write("- Barrios.json")
    st.write("- catalogo_distritos_barrios.csv")

    st.dataframe(df.head(10), use_container_width=True)

    st.download_button(
        "📥 Descargar dataset (CSV)",
        data=df.to_csv(index=False).encode(),
        file_name="distritos_demo.csv"
    )
