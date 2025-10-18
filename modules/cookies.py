import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager


def test():
    # Initialize cookie manager
    cookies = EncryptedCookieManager(
        prefix="myapp_", password="super_secret_key")

    if not cookies.ready():
        st.stop()  # Wait until cookies are ready

    # Try to restore session from cookies
    if "user" not in st.session_state:
        st.session_state.user = cookies.get("user", None)

    st.title("🔐 Persistent Login Example")

    if st.session_state.user:
        st.success(f"Welcome back, {st.session_state.user}!")
        if st.button("Logout"):
            cookies["user"] = ""
            cookies.save()
            del st.session_state.user
            st.rerun()
    else:
        username = st.text_input("Username")
        if st.button("Login"):
            if username:
                # Save to both session and cookies
                st.session_state.user = username
                cookies["user"] = username
                cookies.save()
                st.rerun()
            else:
                st.warning("Please enter a username.")
