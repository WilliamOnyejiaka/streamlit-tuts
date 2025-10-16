import streamlit as st
from components.alert_modal import alert_modal

st.set_page_config(page_title="Sign Up", page_icon="📝", layout="centered")

st.title("📝 Create Your Account")


with st.form("signup_form", clear_on_submit=False):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    access_key = st.text_input("Access Key", type="password")

    submitted = st.form_submit_button("Sign Up")

    if submitted:
        if not full_name or not email or not password:
            alert_modal("Please fill in all fields.")
        elif password != confirm_password:
            alert_modal("Passwords do not match.", level="error")
        else:
            st.session_state.user = True
