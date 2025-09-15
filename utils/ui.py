
import streamlit as st

def inject_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def hero():
    st.markdown("""
    <div class='hero fade-in'>
      <h1>SmartHousing Madrid</h1>
      <p>Encuentra el mejor lugar, en el mejor momento — con datos.</p>
    </div>
    """, unsafe_allow_html=True)

def kpi(title, value, delta=None):
    delta_html = ""
    if isinstance(delta,(int,float)):
        color = "#3FA34D" if delta>=0 else "#AA1927"
        arrow = "↑" if delta>=0 else "↓"
        delta_html = f"<div style='color:{color};font-weight:700'>{arrow} {abs(delta)}%</div>"
    st.markdown(f"""
    <div class='kpi fade-in'>
      <div style='font-size:.9rem;color:#555'>{title}</div>
      <div style='font-size:1.6rem;font-weight:800'>{value}</div>
      {delta_html}
    </div>
    """, unsafe_allow_html=True)

def chip(text):
    st.markdown(f"<span class='chip'>{text}</span>", unsafe_allow_html=True)
