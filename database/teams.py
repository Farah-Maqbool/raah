import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from database.mongo_client import get_database


def get_teams_collection():
    db = get_database()
    return db["teams"]


def assign_team(brief_source_url: str, team_members: list) -> bool:
    """
    Assign a team to a brief.
    team_members = list of email strings
    """
    collection = get_teams_collection()

    existing = collection.find_one({"brief_source_url": brief_source_url})
    if existing:
        return False

    team = {
        "brief_source_url": brief_source_url,
        "members": team_members,
        "status": "assigned",
        "created_at": datetime.utcnow(),
        "pitch_proof": None,
        "hired": None,
        "rejection_reason": None,
        "deliverable": None,
        "verified": False
    }

    collection.insert_one(team)
    return True


def get_team_by_brief(brief_source_url: str) -> dict:
    collection = get_teams_collection()
    team = collection.find_one(
        {"brief_source_url": brief_source_url},
        {"_id": 0}
    )
    return team or {}


def get_teams_by_member(email: str) -> list:
    collection = get_teams_collection()
    return list(collection.find(
        {"members": email},
        {"_id": 0}
    ))


def update_team_status(brief_source_url: str, status: str, extra: dict = {}) -> bool:
    collection = get_teams_collection()
    update = {"status": status, **extra}
    result = collection.update_one(
        {"brief_source_url": brief_source_url},
        {"$set": update}
    )
    return result.modified_count > 0


def save_whatsapp_link(brief_source_url: str, link: str) -> bool:
    collection = get_teams_collection()
    result = collection.update_one(
        {"brief_source_url": brief_source_url},
        {"$set": {"whatsapp_link": link}}
    )
    return result.modified_count > 0


def get_whatsapp_link(brief_source_url: str) -> str:
    collection = get_teams_collection()
    team = collection.find_one({"brief_source_url": brief_source_url})
    return team.get("whatsapp_link", "") if team else ""