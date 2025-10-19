import json
import streamlit as st
from components.alert_modal import alert_modal
from config import ACCESS_KEY, SECRET_KEY
from config.db import db
from modules.CookieManger import CookieManger
from modules.password import hash_password

st.set_page_config(page_title="Sign Up", page_icon="📝", layout="centered")

st.title("📝 Create Your Account")

cookie_manager = CookieManger("myapp_", SECRET_KEY)

if not cookie_manager.ready():
    st.stop()

def create_admin(name: str, email: str, password: str):
    try:
        admin = db["admins"]
        email_exists = admin.find_one({"email": email})
        if not email_exists:
            hashed_password = hash_password(password)
            result = admin.insert_one({
                "name": name,
                "email": email,
                "password": hashed_password
            })

            if result.inserted_id:
                return {"error": False, "message": None, "admin": {
                    "name": name,
                    "email": email,
                    "_id": str(result.inserted_id)
                }}
            return {"error": True, "message": "Something went wrong"}
        else:
            return {"error": True, "message": "Email already exists"}
    except Exception as e:
        return {"error": True, "message": f"Something went wrong: {e}"}


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
        elif access_key != ACCESS_KEY:
            alert_modal("Invalid access key", level="error")
        else:
            result = create_admin(full_name, email, password)
            if result['error']:
                alert_modal(result['message'], level="error")
            else:
                cookie_manager.set("admin", json.dumps(result["admin"]))
                st.switch_page("pages/Dashboard/Tables.py")
