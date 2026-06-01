import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from database.mongo_client import get_database

def get_profiles_collecion():
    db = get_database()
    collection = db["profiles"]

    collection.create_index("email",unique=True)

    return collection

def save_profile(profile:dict) -> bool:
    collection = get_profiles_collecion()
    profile["created_at"] = datetime.now(timezone.utc)

    profile["available"] = True
    profile["completed_projects"] = 0

    try:
        collection.insert_one(profile)
        print(f"saved profile: {profile.get('name')}")

        return True
    except Exception as e:
        if "duplicate key" in str(e).lower():
            print(f"Profile already exists: {profile.get('email')}")
            return False
        print(f"Error saving profile: {e}")
        return False


def get_available_profile():
    collection = get_profiles_collecion()
    return list(collection.find(
        {"available":True},
        {"_id":0}
    ))


def get_profiles_by_skills(skills:list)-> list:
    collection = get_profiles_collecion()
    return list(collection.find(
        {
            "available" : True,
            "skills" : {"$in":skills}
        },
        {"_id":0}
    ))


if __name__ == "__main__":
    # Seed test profiles
    test_profiles = [
        {
            "name": "Ali Hassan",
            "email": "ali@test.com",
            "skills": ["Marketing Strategy", "Social Media", "Content Creation", "Market Research"],
            "field": "Business/Marketing",
            "level": "Undergraduate",
            "university": "LUMS"
        },
        {
            "name": "Sara Ahmed",
            "email": "sara@test.com",
            "skills": ["Data Analysis", "Excel", "Research", "Financial Modeling"],
            "field": "Finance/Data",
            "level": "Undergraduate",
            "university": "IBA"
        },
        {
            "name": "Usman Khan",
            "email": "usman@test.com",
            "skills": ["Python", "Machine Learning", "Data Analysis", "Research"],
            "field": "Computer Science",
            "level": "Undergraduate",
            "university": "NUST"
        },
        {
            "name": "Zara Malik",
            "email": "zara@test.com",
            "skills": ["UI/UX Design", "Figma", "Content Creation", "Social Media"],
            "field": "Design/Media",
            "level": "Undergraduate",
            "university": "NCA"
        },
        {
            "name": "Bilal Raza",
            "email": "bilal@test.com",
            "skills": ["B2B Sales", "Market Research", "Business Strategy", "Communication"],
            "field": "Business",
            "level": "Undergraduate",
            "university": "FAST"
        }
    ]

    print("Seeding test profiles...\n")
    for profile in test_profiles:
        save_profile(profile)

    print(f"\nTotal available profiles: {len(get_available_profile())}")
    print("\nProfiles with Marketing skills:")
    matches = get_profiles_by_skills(["Marketing Strategy", "Market Research"])
    for p in matches:
        print(f"  - {p['name']} | {p['skills']}")
