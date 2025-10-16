import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="My App", layout="wide")

# --- Navbar ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Login", "Sign Up"],
    icons=["house", "box-arrow-in-right", "person-plus"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0E1117"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {
            "color": "white",
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#262730",
        },
        "nav-link-selected": {"background-color": "#00BFFF"},
    },
)

# --- Page logic ---
if selected == "Home":
    st.title("🏠 Home Page")
elif selected == "Login":
    st.title("🔑 Login Page")
elif selected == "Sign Up":
    st.title("📝 Sign Up Page")
