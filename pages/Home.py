import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from components.alert_modal import alert_modal
from config import SECRET_KEY
from modules.CookieManger import CookieManger

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Home Page")

# --- Page setup ---
st.set_page_config(
    page_title="Blumdate DB Viewer",
    page_icon="👋",
    layout="centered"
)

cookie_manager = CookieManger("myapp_", SECRET_KEY)

if not cookie_manager.ready():
    st.stop()
    
# --- Landing Page Content ---
st.title("👋 Welcome to Blumdate DB Viewer")
st.subheader("Your gateway to awesome features 🚀")

st.markdown(
    """
    ### Get started
    Choose what you’d like to do:
    """
)

# --- Action buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔑 Log In"):
        st.switch_page("pages/Auth/Login.py")

with col2:
    if st.button("🏃 Logout"):
        cookie_manager.delete("admin")
        alert_modal("You have been logged out successfully","success")


with col3:
    if st.button("📝 Sign Up"):
        st.switch_page("pages/Auth/SignUp.py")


# --- Optional footer ---
st.markdown("---")
st.caption("© 2025 My Streamlit App — Built with ❤️ by William")
