import streamlit as st

st.set_page_config(page_title="Blumdate DB Viewer", layout="wide")

# Define navigation
nav = st.navigation(
    {
        "Home": [st.Page("pages/Home.py", title="🏠 Home")],
        "Auth": [
            st.Page("pages/Auth/Login.py", title="🔑 Login"),
            st.Page("pages/Auth/SignUp.py", title="📝 Sign Up")
        ],
        "Dashboard": [
            st.Page("pages/Dashboard/Tables.py", title="🗃 Tables"),
        ]
    },
    # position="top"  # 👈 This puts it as a top navbar
)

# Run the selected page
nav.run()
