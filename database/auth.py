import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from database.mongo_client import get_database

def get_users_collection():
    db = get_database()
    collection = db["users"]
    collection.create_index("email", unique=True)
    return collection

def signup_user(name, email, password, university, field, level, skills) -> dict:
    collection = get_users_collection()

    # Check if email exists
    if collection.find_one({"email": email}):
        return {"success": False, "message": "Email already registered."}

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user = {
        "name": name,
        "email": email,
        "password": hashed,
        "university": university,
        "field": field,
        "level": level,
        "skills": skills,
        "available": True,
        "completed_projects": 0
    }

    try:
        collection.insert_one(user)
        return {"success": True, "message": "Account created."}
    except Exception as e:
        return {"success": False, "message": str(e)}


def login_user(email, password) -> dict:
    collection = get_users_collection()
    user = collection.find_one({"email": email})

    if not user:
        return {"success": False, "message": "No account found with this email."}

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return {"success": False, "message": "Incorrect password."}

    return {
        "success": True,
        "user": {
            "name": user["name"],
            "email": user["email"],
            "field": user["field"],
            "university": user.get("university", ""),
            "skills": user.get("skills", []),
            "level": user.get("level", ""),
            "completed_projects": user.get("completed_projects", 0)
        }
    }


def get_user_by_email(email) -> dict:
    collection = get_users_collection()
    user = collection.find_one({"email": email}, {"password": 0, "_id": 0})
    return user or {}