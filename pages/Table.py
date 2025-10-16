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
# 🧹 Data Cleaning Function
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
# 📑 Pagination Function
# =========================
def paginate_dataframe(df, page_size=10):
    total_pages = max(1, (len(df) + page_size - 1) // page_size)
    page = st.number_input(
        "Page", min_value=1, max_value=total_pages, value=1, key=f"page_{df.columns[0]}")
    start = (page - 1) * page_size
    end = start + page_size
    return df.iloc[start:end]


# =========================
# 🧭 Navigation Tabs
# =========================
collections = {
    "Users": db["users"],
    "Orders": db["orders"],
    "Products": db["products"]
}

st.title("📊 MongoDB Dashboard with Delete Option")

tabs = st.tabs(list(collections.keys()))


# =========================
# 🧾 Render Each Collection
# =========================
for i, (name, collection) in enumerate(collections.items()):
    with tabs[i]:
        st.subheader(f"📁 {name} Collection")

        data = list(collection.find())
        if not data:
            st.info("No data available.")
            continue

        cleaned_data = clean_mongo_docs(data)
        df = pd.DataFrame(cleaned_data)

        paginated_df = paginate_dataframe(df)

        st.dataframe(paginated_df, use_container_width=True)

        # Delete form
        st.write("### 🗑️ Delete Record")
        delete_id = st.text_input(
            f"Enter {name} _id to delete:", key=f"delete_{name}")

        if st.button(f"Delete from {name}", key=f"delete_btn_{name}"):
            if delete_id:
                result = collection.delete_one({"_id": delete_id})
                if result.deleted_count > 0:
                    st.success(f"✅ Deleted record with _id: {delete_id}")
                    st.rerun()  # Refresh page
                else:
                    st.warning(f"⚠️ No record found with _id: {delete_id}")
            else:
                st.error("Please enter a valid _id before deleting.")
