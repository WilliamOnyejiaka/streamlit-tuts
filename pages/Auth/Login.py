import streamlit as st
from components.alert_modal import alert_modal
from config import SECRET_KEY
from config.db import db
from modules.password import verify_password
import json
from modules.CookieManger import CookieManger

st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

cookie_manager = CookieManger("myapp_", SECRET_KEY)

if not cookie_manager.ready():
    st.stop()

st.title("🔑 Login To Your Account")

def login_admin(email: str, password: str):
    try:
        collection = db["admins"]
        admin = collection.find_one({"email": email})
        if admin:
            valid_password = verify_password(password, admin['password'])
            admin["_id"] = str(admin["_id"])
            del admin['password']
            return {"error": False, "message": None, "admin": admin} if valid_password else {"error": True, "message": "Invalid password"}
        else:
            return {"error": True, "message": "Admin was not found"}
    except Exception as e:
        return {"error": True, "message": f"Something went wrong: {e}"}


with st.form("login", clear_on_submit=False):
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Login")

    st.page_link("pages/Auth/SignUp.py",
                 label="📝 Don’t have an account? Sign up",)

    if submitted:
        if not email or not password:
            alert_modal("Please fill in all fields.")
        else:
            result = login_admin(email, password)

            if result['error']:
                alert_modal(result['message'], level="error")
            else:
                cookie_manager.set("admin", json.dumps(result['admin']))
                st.switch_page("pages/Dashboard/Tables.py")
