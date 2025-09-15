
import streamlit as st
import numpy as np
import pandas as pd
import json
import joblib
from utils.ui import inject_css
import shap

st.set_page_config(page_title="Calculadora con bandas", layout="wide", page_icon="🧭")
inject_css()
st.title("Calculadora de precio con bandas de confianza (P10–P90)")

FEATURE_COLUMNS_PATH = "models/feature_columns.json"   # derivado de columns.json
PREPROCESSOR_PATH    = "models/preprocessor.pkl"       # opcional
MODEL_P10_PATH       = "models/model_p10.pkl"
MODEL_P50_PATH       = "models/model_p50.pkl"
MODEL_P90_PATH       = "models/model_p90.pkl"
SHAP_EXPLAINER_PATH  = "models/shap_explainer.pkl"     # opcional

@st.cache_resource(show_spinner=False)
def load_artifacts():
    with open(FEATURE_COLUMNS_PATH, "r") as f:
        feature_columns = json.load(f)
    preproc = None
    try:
        preproc = joblib.load(PREPROCESSOR_PATH)
    except Exception:
        pass
    model_p10 = joblib.load(MODEL_P10_PATH)
    model_p50 = joblib.load(MODEL_P50_PATH)
    model_p90 = joblib.load(MODEL_P90_PATH)
    shap_explainer = None
    try:
        shap_explainer = joblib.load(SHAP_EXPLAINER_PATH)
    except Exception:
        shap_explainer = None
    return feature_columns, preproc, model_p10, model_p50, model_p90, shap_explainer

def safe_load():
    try:
        return load_artifacts()
    except Exception as e:
        st.error(f"⚠️ No se pudieron cargar los artefactos del modelo. {e}")
        st.stop()

feature_columns, preproc, model_p10, model_p50, model_p90, shap_explainer = safe_load()

col1, col2, col3 = st.columns(3)
with col1:
    distrito = st.selectbox("Distrito", [
        "Centro","Arganzuela","Retiro","Salamanca","Chamartín","Tetuán","Chamberí",
        "Fuencarral-El Pardo","Moncloa-Aravaca","Latina","Carabanchel","Usera",
        "Puente de Vallecas","Moratalaz","Ciudad Lineal","Hortaleza","Villaverde",
        "Villa de Vallecas","Vicálvaro","San Blas-Canillejas","Barajas"
    ])
    superficie = st.number_input("Superficie (m²)", 20, 400, 85)
with col2:
    habitaciones = st.selectbox("Habitaciones", [1,2,3,4])
    ascensor = st.selectbox("Ascensor", ["Sí","No"], index=0)
with col3:
    cerca_metro = st.selectbox("Cercanía a Metro", ["Sí","No"], index=0)
    antiguedad = st.slider("Antigüedad (años)", 0, 120, 35)

def build_row():
    base = {fc: 0 for fc in feature_columns}
    mapping = {
        "DISTRITO_x": distrito,                 # usa nombres de columns.json
        "BARRIO": distrito,                     # si el modelo lo requiere, puedes mapear con catálogo
        "TIPO_VIVIENDA": "Total",               # valor por defecto
        "PRECIO_EUR_M2_x": 0,                   # no introducir el target aquí
        "Tamaño medio del hogar": 2.6,
        "Población densidad (hab./Ha.)": 150.0,
        "Tasa absoluta de paro registrado (febrero)": 8.5,
        "Índice de Seguridad por 1000 habitantes (Robusto 1-10)": 6.8,
        "Relación de Superficie de zonas verdes y Parques de distrito (ha) entre número de Habitantes *10.000": 2.1,
        # ... el resto quedará en 0 o defaults; idealmente rellena desde medias distritales
        "superficie": superficie,
        "habitaciones": habitaciones,
        "ascensor": 1 if ascensor=="Sí" else 0,
        "cercania_metro": 1 if cerca_metro=="Sí" else 0,
        "antiguedad": antiguedad,
    }
    for k,v in mapping.items():
        if k in base:
            base[k]=v
    return pd.DataFrame([base])[feature_columns]

if st.button("Calcular bandas P10–P90", use_container_width=True):
    X = build_row()
    try:
        Xp = preproc.transform(X) if preproc is not None else X
        y10 = float(model_p10.predict(Xp)[0])
        y50 = float(model_p50.predict(Xp)[0])
        y90 = float(model_p90.predict(Xp)[0])
        st.success(f"Mediana: **{y50:,.0f} €/m²** · Intervalo **[{y10:,.0f}–{y90:,.0f}] €/m²**")
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Indicator(mode="number+gauge+delta",
                                   value=y50, number={'suffix':" €/m²"},
                                   delta={'reference': y10, 'increasing': {'color': '#3FA34D'}, 'decreasing': {'color': '#AA1927'}},
                                   gauge={'shape': "bullet",
                                          'axis': {'range': [max(0,y10*0.8), y90*1.2]},
                                          'bar': {'color':'#1B3B6F'},
                                          'threshold': {'line': {'color': "#AA1927", 'width': 3}, 'thickness': 0.75, 'value': y90}},
                                   domain={'x':[0,1],'y':[0,1]}))
        fig.update_layout(height=140, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error en inferencia: {e}")

    st.markdown('---')
    st.subheader("¿Por qué esta predicción? (SHAP)")
    try:
        # Intento cargar explainer
        try:
            explainer = joblib.load(SHAP_EXPLAINER_PATH)
        except Exception:
            explainer = shap.Explainer(model_p50)
        X_for = X if isinstance(X, pd.DataFrame) else pd.DataFrame(X, columns=feature_columns)
        shap_vals = explainer(X_for)
        importances = np.abs(shap_vals.values[0])
        top_idx = np.argsort(importances)[::-1][:5]
        top_feats = [feature_columns[i] for i in top_idx]
        top_vals  = importances[top_idx]
        import plotly.express as px
        fig_imp = px.bar(x=top_vals[::-1], y=top_feats[::-1], orientation="h", title="Impacto de variables (SHAP | abs)")
        st.plotly_chart(fig_imp, use_container_width=True)
    except Exception as e:
        st.info("SHAP no disponible. Puedes guardar 'models/shap_explainer.pkl'.")
        st.caption(f"Detalle: {e}")
