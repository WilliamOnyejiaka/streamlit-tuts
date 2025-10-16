import streamlit as st

@st.dialog("Alert")
def alert_modal(message, level="info"):
    if level == "warning":
        st.warning(message)
    elif level == "error":
        st.error(message)
    else:
        st.info(message)
