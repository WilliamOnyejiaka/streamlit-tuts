import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# =========================
# 🔗 MongoDB Connection
# =========================
# MONGO_URI = "mongodb://localhost:27017"
# DB_NAME = "blumdate_db"

MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = st.secrets["DB_NAME"]


client = MongoClient(MONGO_URI)
db = client[DB_NAME]


# =========================
# 🧹 Data Cleaning
# =========================
def clean_mongo_docs(docs):
    cleaned = []
    for doc in docs:
        doc["_id"] = str(doc.get("_id", ""))  # Convert ObjectId
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

st.title("📊 MongoDB Dashboard (With Inline Delete Buttons)")

tabs = st.tabs(list(collections.keys()))


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

        paginated_df = paginate_dataframe(df, key_prefix=name)

        # Display with delete buttons
        for index, row in paginated_df.iterrows():
            with st.container():
                cols = st.columns([5, 1])
                cols[0].write(row.to_dict())
                if cols[1].button("🗑️", key=f"delete_{name}_{row['_id']}"):
                    result = collection.delete_one({"_id": row["_id"]})
                    if result.deleted_count > 0:
                        st.success(f"Deleted record: {row['_id']}")
                        st.rerun()
                    else:
                        st.warning("No record deleted.")
                st.divider()
