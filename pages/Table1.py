import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# =========================
# 🔗 MongoDB Connection
# =========================
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "blumdate_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


# =========================
# 🧹 Data Cleaning
# =========================
def clean_mongo_docs(docs):
    cleaned = []
    for doc in docs:
        doc["_id"] = str(doc.get("_id", ""))  # Convert ObjectId to string
        for key, value in doc.items():
            if isinstance(value, (list, dict)):
                doc[key] = str(value)
            elif isinstance(value, datetime):
                doc[key] = value.isoformat()
        cleaned.append(doc)
    return cleaned


# =========================
# 📑 Pagination
# =========================
def paginate_dataframe(df, page_size=10, key_prefix=""):
    total_pages = max(1, (len(df) + page_size - 1) // page_size)
    page = st.number_input(
        "Page", min_value=1, max_value=total_pages, value=1, key=f"page_{key_prefix}"
    )
    start = (page - 1) * page_size
    end = start + page_size
    return df.iloc[start:end]


# =========================
# 🧭 Collections
# =========================
collections = {
    "Users": db["users"],
    "Orders": db["orders"],
    "Products": db["products"]
}

st.title("📊 MongoDB Dashboard (Table + Delete + Modal)")

tabs = st.tabs(list(collections.keys()))


@st.dialog("Confirm Deletion")
def alert_modal(collection, delete_id, level="info"):
    st.warning(
        f"Are you sure you want to delete record `{delete_id}`?")
    confirm = st.button("✅ Yes, Delete")
    cancel = st.button("❌ Cancel")

    if confirm:
        result = collection.delete_one({"_id": delete_id})
        if result.deleted_count > 0:
            st.success(f"Deleted record: {delete_id}")
            st.rerun()
        else:
            st.error("Failed to delete.")
    elif cancel:
        st.rerun()


# =========================
# 🧾 Render Each Collection
# =========================
for i, (name, collection) in enumerate(collections.items()):
    with tabs[i]:
        st.subheader(f"📁 {name} Collection")

        data = list(collection.find())
        if not data:
            st.info("No data found in this collection.")
            continue

        cleaned_data = clean_mongo_docs(data)
        df = pd.DataFrame(cleaned_data)

        # Add delete column
        df["Delete"] = False

        paginated_df = paginate_dataframe(df, key_prefix=name)

        # Editable table with checkboxes
        edited_df = st.data_editor(
            paginated_df,
            use_container_width=True,
            hide_index=True,
            key=f"editor_{name}"
        )

        # Handle deletions
        if edited_df["Delete"].any():
            to_delete = edited_df[edited_df["Delete"] == True]
            for _, row in to_delete.iterrows():
                delete_id = row["_id"]
                
                alert_modal(collection,delete_id)
                # Confirmation modal
                # with st.dialog("Confirm Deletion"):
                #     st.warning(
                #         f"Are you sure you want to delete record `{delete_id}`?")
                #     confirm = st.button("✅ Yes, Delete")
                #     cancel = st.button("❌ Cancel")

                #     if confirm:
                #         result = collection.delete_one({"_id": delete_id})
                #         if result.deleted_count > 0:
                #             st.success(f"Deleted record: {delete_id}")
                #             st.rerun()
                #         else:
                #             st.error("Failed to delete.")
                #     elif cancel:
                #         st.rerun()
