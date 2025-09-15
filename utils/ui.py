
import streamlit as st
import os
import base64

def inject_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def hero():
    """
    Render a hero section with a subtle background illustration and a tagline.

    The hero pulls in a pastel cityscape illustration from the ``assets``
    folder at runtime and encodes it to base64 so it can be inlined in the
    HTML. This avoids any external network calls and guarantees the image
    will load instantly. A semi‑transparent gradient overlay ensures
    readability of the headline and subheading. The entire block also uses
    the existing ``fade-in`` animation for a smooth entry.
    """
    # Compute the absolute path to our hero image and base64‑encode it. Using
    # ``os.path.join`` makes this robust to being called from different
    # working directories.
    # Build an absolute path to the hero illustration. We resolve the path
    # relative to this file so it works regardless of the current working
    # directory when Streamlit runs. The image lives in ``app/assets``.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Use the refreshed hero background to emphasise the new colour palette.
    image_path = os.path.join(base_dir, "..", "assets", "hero_background_new.png")
    try:
        with open(image_path, "rb") as f:
            encoded_bg = base64.b64encode(f.read()).decode()
        bg_style = (
            f"background-image: url('data:image/png;base64,{encoded_bg}'); "
            "background-size: cover; background-position: center;"
        )
    except Exception:
        # Fallback to a blue gradient if the image can't be read.
        bg_style = "background:linear-gradient(135deg, var(--brand-dark), #2171c2);"

    # Load the logo from the assets folder and encode it to base64.
    logo_path = os.path.join(base_dir, "..", "assets", "logo.png")
    encoded_logo = ""
    try:
        with open(logo_path, "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode()
    except Exception:
        encoded_logo = ""

    # Compose the HTML for the hero. We embed the background style directly
    # into the div. The gradient overlay lives in a child div with its own
    # class. If the logo is available, it will be displayed above the heading.
    logo_html = f"<img src='data:image/png;base64,{encoded_logo}' class='logo' alt='Logo' />" if encoded_logo else ""
    html = f"""
    <div class='hero fade-in' style="{bg_style}">
      <div class='hero-overlay'></div>
      {logo_html}
      <h1>SmartHousing Madrid</h1>
      <p>Encuentra el mejor lugar, en el mejor momento — con datos.</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

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
