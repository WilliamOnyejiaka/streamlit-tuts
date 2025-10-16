import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="MongoDB Data Viewer", layout="wide")

# --- MongoDB Connection ---
MONGO_URI = "mongodb://localhost:27017"  # Replace with your actual URI
DB_NAME = "blumdate_db"


@st.cache_resource
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]


db = get_db()

# --- Page Layout ---
st.title("📊 MongoDB Data Viewer")

# List available collections
collections = db.list_collection_names()
selected_collection = st.selectbox("Choose a collection", collections)

# --- Pagination Settings ---
PAGE_SIZE = st.sidebar.number_input(
    "Items per page", min_value=5, max_value=100, value=10, step=5)

# Use session_state to track current page
if "page_number" not in st.session_state:
    st.session_state.page_number = 1

# Function to reset pagination when collection changes


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
        # Convert ObjectId to string
        for doc in data:
            doc["_id"] = str(doc["_id"])

        df = pd.DataFrame(data)
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

        # --- Optional: Download current page ---
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download this page as CSV",
            data=csv,
            file_name=f"{selected_collection}_page{st.session_state.page_number}.csv",
            mime="text/csv",
        )
