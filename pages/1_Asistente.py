
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.ui import inject_css, chip

st.set_page_config(page_title="Flujo Usuario", layout="wide", page_icon="🧭")
inject_css()
st.title("Asistente — Encuentra tu mejor lugar y momento")

if "objetivo" not in st.session_state:
    st.session_state["objetivo"] = "comprar"
st.write(f"**Objetivo:** {st.session_state['objetivo'].capitalize()}")

# Paso 1: preferencias
# Paso 1: preferencias
with st.expander("① Presupuesto y necesidades", expanded=True):
    c1, c2 = st.columns([2,1])
    with c1:
        presupuesto = st.slider("Presupuesto máximo (€)", 120000, 1200000, 350000, 10000)
        habitaciones = st.selectbox("Habitaciones", [1,2,3,4], index=1)
        prioridades = st.multiselect(
            "Prioridades",
            ["Precio bajo", "Zonas verdes", "Transporte", "Seguridad", "Inversión"],
            default=["Precio bajo", "Transporte"],
        )
        st.write("**Tus prioridades:**")
        for p in prioridades:
            chip(p)
    with c2:
        st.info(
            "Ajusta tus prioridades para perfilar la búsqueda. Te mostraremos zonas que encajan con tu perfil y presupuesto."
        )

# Paso 2: recomendaciones (demo con CSV de distritos_madrid_coords si existe)
st.markdown("---")
st.subheader("② Recomendaciones")
try:
    df = pd.read_csv("data/distritos_madrid_coords.csv")
except Exception:
    df = pd.DataFrame({
        "distrito":["Chamartín","Hortaleza","Puente de Vallecas","Arganzuela","Centro","Tetuán"],
        "precio_m2":[4650,3970,2120,4300,5200,3600],
        "variacion_interanual":[5.2,1.8,-0.5,3.1,4.7,0.9],
        "lat":[40.449,40.478,40.387,40.399,40.418,40.458],
        "lon":[-3.677,-3.642,-3.659,-3.700,-3.703,-3.703]
    })

df["score"] = (df["variacion_interanual"].rank(ascending=False) + df["precio_m2"].rank(ascending=True))
df_top = df.sort_values("score").head(3)

cards = st.columns(3)
for i, (_, row) in enumerate(df_top.iterrows()):
    with cards[i]:
        # Determine colour of trend (green/up, yellow/flat, red/down)
        color = (
            "#3FA34D"
            if row["variacion_interanual"] > 2
            else ("#E1A500" if row["variacion_interanual"] > -0.3 else "#AA1927")
        )
        # Render a custom card with slide up and incremental delays
        st.markdown(
            f"""
            <div class="district-card slide-up delay-{i+1}">
              <div class="district-name">{row['distrito']}</div>
              <div class="district-price">{int(row['precio_m2']):,} €/m²</div>
              <div class="district-trend" style="color:{color};">{row['variacion_interanual']}% tendencia</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Generate a small synthetic trend line for the card below
        y = np.cumsum(np.random.randn(24)) * 5 + row["precio_m2"]
        fig = px.line(
            x=list(range(24)),
            y=y,
            labels={"x": "meses", "y": "€/m²"},
        )
        fig.update_layout(height=120, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

# Paso 3: Cuándo — Momento ideal con banda (demo de proyección sintética)
st.markdown("---")
st.subheader("③ Momento ideal (demo)")
sel = st.selectbox("Ver proyección para:", df_top["distrito"].tolist())
base = float(df.loc[df["distrito"]==sel,"precio_m2"].iloc[0]) if sel in df["distrito"].values else 4000.0
meses = np.arange(0,24)
trend = base*(1+0.002*meses)  # demo
noise = np.linspace(-80,80,24)
p50 = trend + noise
p10 = p50 - 150
p90 = p50 + 150

fig2 = px.line(x=meses, y=p50, labels={"x":"Meses adelante","y":"€/m²"}, title=f"Proyección {sel} (P10–P90)")
fig2.add_traces([px.line(x=meses, y=p10).data[0], px.line(x=meses, y=p90).data[0]])
fig2.update_traces(showlegend=False)
fig2.add_traces(px.area(x=list(meses)+list(meses[::-1]), y=list(p90)+list(p10[::-1])).update_traces(opacity=0.15).data)
st.plotly_chart(fig2, use_container_width=True)
st.info("En producción: esta banda vendrá de tus modelos cuantílicos (P10, P50, P90) por distrito o de un modelo panel.")

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("📥 Descargar recomendaciones (PDF/CSV)", use_container_width=True):
        st.success("Descarga generada (demo).")
with c2:
    if st.button("🔍 Pasar a Calculadora con bandas", use_container_width=True):
        st.switch_page("pages/3_Calculadora_Bandas.py")
