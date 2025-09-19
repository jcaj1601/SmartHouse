import streamlit as st

st.set_page_config(page_title="Power BI", layout="wide", page_icon="📊")
st.title("📊 Dashboard Power BI")

st.markdown(
    """
    <iframe title="VIVIENDA MADRID_TFM5" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=45d8552b-4b9f-4300-b162-925740278d39&autoAuth=true&ctid=2b079dc7-e2ea-45bc-9182-0fde14b549b1" frameborder="0" allowFullScreen="true"></iframe>
    """,
    unsafe_allow_html=True
)
