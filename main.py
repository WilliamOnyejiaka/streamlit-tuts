import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

# Define navigation
nav = st.navigation(
    {
        "Home": [st.Page("Home.py", title="🏠 Home")],
        "Auth": [
            st.Page("pages/Auth/Login.py", title="🔑 Login"),
            st.Page("pages/Auth/SignUp.py", title="📝 Sign Up")
        ],
        "Dashboard": [
            st.Page("pages/Dashboard.py", title="🏠 Dashboard"),
            st.Page("pages/Table.py", title="🏠 Table"),
            st.Page("pages/Table2.py", title="🏠 Table2"),
            st.Page("pages/Table1.py", title="🏠 Table1")

        ]
    },
    # position="top"  # 👈 This puts it as a top navbar

)

# Run the selected page
nav.run()
