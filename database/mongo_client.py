import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st

load_dotenv()



def get_database():
    # Try Streamlit secrets first, then .env
    try:
        uri = st.secrets["MONGODB_URI"]
    except Exception:
        uri = os.getenv("MONGODB_URI")

    if not uri:
        raise ValueError("MONGODB_URI not found")

    client = MongoClient(uri, tlsCAFile=certifi.where())
    return client["raah"]

def get_opportunities_collection():
    db = get_database()
    collection = db["opportunities"]
    collection.create_index("source_url", unique=True)
    return collection


if __name__ == "__main__":
    try:
        db = get_database()
        print("MongoDB connected successfully")
        print(f"Database: {db.name}")
    except Exception as e:
        print(f"Connection failed: {e}")