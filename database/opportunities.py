import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from database.mongo_client import get_opportunities_collection


def save_brief(brief: dict) -> bool:
    """
    Save a brief to MongoDB.
    Returns True if saved, False if duplicate.
    """

    collection =get_opportunities_collection()

    brief["created_at"] = datetime.now(timezone.utc)
    brief["status"] = "open"

    try:
        collection.insert_one(brief)
        print(f"Saved: {brief.get('title', 'Unknown')}")
        return True

    except Exception as e:
        if "duplicate key" in str(e).lower():
            print(f"Skipped duplicate: {brief.get('source_url', 'Unknown URL')}")
            return False
        print(f"Error Saving: {e}")
        return False


def get_open_briefs() -> list:
    """Get all open briefs available for teams"""

    collection = get_opportunities_collection()
    return list(collection.find({"status":"open"},{"_id":0}))

def brief_exists(source_url: str) -> bool:
    """Check if brief with this URL already exists."""
    collection = get_opportunities_collection()
    return collection.find_one({"source_url":source_url}) is not None

if __name__ == "__main__":
    test_brief = {
        "title" : "Test brief",
        "source_url": "https://reddit.com/test/123",
        "problem": "Test problem",
        "skills_needed": ["Python", "Research"],
        "difficulty": "Beginner"
    }

    result = save_brief(test_brief)
    print(f"Saved: {result}")

    briefs = get_open_briefs()
    print(f"Total open briefs: {len(briefs)}")