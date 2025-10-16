import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Home Page")

# if "user" not in st.session_state or not st.session_state.user:
#     st.warning("You’re not logged in! Go to the Login page.")
#     # st.page_link("Login.py", label="Go to Login")
#     # st.page_link("pages/SignUp.py", label="Go to Profile")
#     st.switch_page("pages/SignUp.py")  # ✅ CORRECT
# else:
#     st.success(f"Welcome back, {st.session_state.user}!")
#     # st.page_link("pages/SignUp.py", label="Go to Profile")


# # --- Page setup ---
# st.set_page_config(
#     page_title="Welcome to My App",
#     page_icon="👋",
#     layout="centered"
# )

# # --- Landing Page Content ---
# st.title("👋 Welcome to My App")
# st.subheader("Your gateway to awesome features 🚀")

# st.markdown(
#     """
#     ### Get started
#     Choose what you’d like to do:
#     """
# )

# # --- Action buttons ---
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("🔑 Log In"):
#         st.switch_page("pages/Login.py")

# with col2:
#     if st.button("📝 Sign Up"):
#         st.switch_page("pages/SignUp.py")

# # --- Optional footer ---
# st.markdown("---")
# st.caption("© 2025 My Streamlit App — Built with ❤️ by William")
