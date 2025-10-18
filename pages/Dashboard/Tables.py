import streamlit as st
import pandas as pd
from config.db import db
from modules.clean_mongo_docs import clean_mongo_docs
from bson import ObjectId

st.set_page_config(page_title="MongoDB Data Viewer",
                   page_icon="🗃", layout="wide")

# --- Page Layout ---
st.title("📊 MongoDB Data Viewer")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("You’re not logged in! Go to the Login page.")
    st.switch_page("pages/Auth/Login.py")  # ✅ CORRECT

# List available collections
collections = db.list_collection_names()
selected_collection = st.selectbox("Choose a collection", collections)

# --- Pagination Settings ---
PAGE_SIZE = st.sidebar.number_input(
    "Items per page", min_value=5, max_value=100, value=10, step=5)

# Use session_state to track current page
if "page_number" not in st.session_state:
    st.session_state.page_number = 1


def reset_page():
    st.session_state.page_number = 1


# Reset when collection changes
if st.session_state.get("last_collection") != selected_collection:
    st.session_state.last_collection = selected_collection
    reset_page()

# --- Load data with pagination ---
if selected_collection:
    collection = db[selected_collection]
    total_docs = collection.count_documents({})

    skip = (st.session_state.page_number - 1) * PAGE_SIZE
    cursor = collection.find().skip(skip).limit(PAGE_SIZE)
    data = list(cursor)

    if not data:
        st.warning("No data found.")
    else:
        df = pd.DataFrame(clean_mongo_docs(data))
        st.dataframe(df, use_container_width=True)

        # --- Pagination Controls ---
        total_pages = max(1, (total_docs + PAGE_SIZE - 1) // PAGE_SIZE)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Prev") and st.session_state.page_number > 1:
                st.session_state.page_number -= 1
                st.rerun()
        with col2:
            st.markdown(
                f"<div style='text-align:center;'>Page {st.session_state.page_number} of {total_pages}</div>",
                unsafe_allow_html=True
            )
        with col3:
            if st.button("Next ➡️") and st.session_state.page_number < total_pages:
                st.session_state.page_number += 1
                st.rerun()

        # Delete form
        name = selected_collection
        st.write("### 🗑️ Delete Record")
        delete_id = st.text_input(
            f"Enter {name} _id to delete:", key=f"delete_{name}")

        if st.button(f"Delete from {name}", key=f"delete_btn_{name}"):
            if delete_id:
                result = collection.delete_one({"_id": ObjectId(delete_id)})
                if result.deleted_count > 0:
                    st.success(f"✅ Deleted record with _id: {delete_id}")
                    st.rerun()  # Refresh page
                else:
                    st.warning(f"⚠️ No record found with _id: {delete_id}")
            else:
                st.error("Please enter a valid _id before deleting.")
