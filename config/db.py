import streamlit as st
from pymongo import MongoClient

MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = st.secrets["DB_NAME"]


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
