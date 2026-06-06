import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from database.mongo_client import get_database


def get_messages_collection():
    db = get_database()
    return db["messages"]


def send_message(brief_source_url: str, sender_email: str, sender_name: str, text: str) -> bool:
    collection = get_messages_collection()
    message = {
        "brief_source_url": brief_source_url,
        "sender_email": sender_email,
        "sender_name": sender_name,
        "text": text,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(message)
    return True


def get_messages(brief_source_url: str) -> list:
    collection = get_messages_collection()
    return list(collection.find(
        {"brief_source_url": brief_source_url},
        {"_id": 0}
    ).sort("timestamp", 1))
