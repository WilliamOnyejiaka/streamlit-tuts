import streamlit as st
from components.alert_modal import alert_modal

st.set_page_config(page_title="Login", page_icon="📝", layout="centered")

st.title("📝 Login To Your Account")


with st.form("login", clear_on_submit=False):
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Login")

    # st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.page_link("pages/Auth/SignUp.py",
                 label="📝 Don’t have an account? Sign up",)
    # st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not email or not password:
            alert_modal("Please fill in all fields.")
        else:
            st.session_state.user = True
            st.switch_page("pages/Dashboard.py")
