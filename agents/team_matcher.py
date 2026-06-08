import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import re
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.genai import types
from database.opportunities import get_open_briefs
from database.auth import get_all_users
from database.teams import assign_team, get_team_by_brief, get_teams_by_member

load_dotenv()


def get_open_briefs_tool():
    """Get all open briefs from MongoDB."""
    briefs = get_open_briefs()
    if not briefs:
        return "No open briefs found."
    output = ""
    for i, brief in enumerate(briefs):
        output += f"BRIEF {i+1}:\n"
        output += f"PROBLEM: {brief.get('problem', 'N/A')}\n"
        output += f"SKILLS NEEDED: {brief.get('skills_needed', [])}\n"
        output += f"DIFFICULTY: {brief.get('difficulty', 'N/A')}\n"
        output += f"BRIEF_ID: {brief.get('source_url', 'N/A')}\n"
        output += "---\n"
    return output


def get_available_profile_tool():
    """Get all available graduate profiles from MongoDB."""
    profiles = get_all_users()
    if not profiles:
        return "No available profiles found."
    output = ""
    for i, profile in enumerate(profiles):
        output += f"PROFILE {i+1}:\n"
        output += f"NAME: {profile.get('name', 'N/A')}\n"
        output += f"SKILLS: {profile.get('skills', [])}\n"
        output += f"FIELD: {profile.get('field', 'N/A')}\n"
        output += f"EMAIL: {profile.get('email', 'N/A')}\n"
        output += "---\n"
    return output


def parse_and_save_matches(raw_output: str):
    """
    Parse team matcher output and save assignments to MongoDB.
    Uses BRIEF_ID directly — no fuzzy matching.
    """
    saved = 0
    blocks = re.split(r"MATCH\s+\d+:", raw_output)

    for block in blocks:
        if not block.strip():
            continue

        # Extract BRIEF_ID directly
        id_match = re.search(r"BRIEF_ID:\s*(.+)", block)
        if not id_match:
            print("No BRIEF_ID found in block — skipping")
            continue

        source_url = id_match.group(1).strip()

        if not source_url or source_url == "N/A":
            print("Invalid BRIEF_ID — skipping")
            continue

        # Check if team already assigned to this brief
        existing = get_team_by_brief(source_url)
        if existing:
            print(f"Team already assigned — skipping: {source_url[:50]}")
            continue

        # Extract emails
        emails = re.findall(r"\|\s*([\w.+-]+@[\w.-]+\.\w+)\s*\|", block)

        if not emails:
            print(f"No emails found — skipping: {source_url[:50]}")
            continue

        # Remove people already in an active team
        available = []
        for email in emails:
            existing_teams = get_teams_by_member(email)
            active = [t for t in existing_teams if t.get("status") not in ["submitted", "verified", "rejected"]]
            if not active:
                available.append(email)
            else:
                print(f"{email} already in active team — skipping")

        if not available:
            print(f"No available members for brief — skipping")
            continue

        # Enforce max 4
        available = available[:4]

        success = assign_team(source_url, available)
        if success:
            print(f"Team saved: {available} -> {source_url[:50]}")
            saved += 1
        else:
            print(f"Failed to save: {source_url[:50]}")

    print(f"\nTotal teams saved: {saved}")


team_matcher = Agent(
    name="team_matcher",
    model=LiteLlm(model="groq/llama-3.3-70b-versatile"),
    instruction="""
You are TeamMatcher — an agent inside Raah that matches real business
problems to the right student teams.

YOUR JOB:
1. Use get_open_briefs_tool to get all open business problems
2. Use get_available_profile_tool to get all available graduates
3. For each brief — find 1 to 4 graduates whose skills match best
4. Form a team for each brief

MATCHING RULES:
- Match skills needed in the brief to skills listed in profiles
- A team should have complementary skills — not all the same
- Minimum 1 person — assign even if only one person matches
- Maximum 4 people — never exceed 4
- Each person can only be in one team at a time
- If no match exists at all — say "No match found" for that brief

CRITICAL — BRIEF_ID RULE:
The BRIEF_ID field in the tool output contains a long URL starting with 
https://vertexaisearch.cloud.google.com or https://reddit.com or similar.
Copy it CHARACTER FOR CHARACTER. Do not shorten it. Do not replace it with 
a different URL. Do not make up a URL. Copy exactly what the tool returned.

CRITICAL: In your output you MUST include BRIEF_ID copied exactly from the brief data.
This is used to save the assignment. If BRIEF_ID is missing the assignment will not save.

OUTPUT FORMAT — follow exactly:

MATCH [number]:
BRIEF: [problem statement]
BRIEF_ID: [copy BRIEF_ID exactly as given in brief data — do not modify]
SKILLS NEEDED: [skills from brief]
TEAM:
  - [Name] | [Email] | [Matching skills]
  - [Name] | [Email] | [Matching skills]
REASON: [one sentence]
---
    """,
    tools=[
        FunctionTool(get_open_briefs_tool),
        FunctionTool(get_available_profile_tool)
    ],
    description="Matches open briefs to available graduate profiles."
)


async def run_team_matcher():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        state={},
        app_name="raah",
        user_id="matcher_user"
    )

    runner = Runner(
        app_name="raah",
        agent=team_matcher,
        session_service=session_service
    )

    content = types.Content(
        role="user",
        parts=[types.Part(
            text="Match all open briefs to available graduate teams."
        )]
    )

    print("\nTEAM MATCHER RUNNING...\n")
    print("=" * 60)

    final_output = ""

    async for event in runner.run_async(
        user_id="matcher_user",
        session_id=session.id,
        new_message=content
    ):
        if (event.content is not None and
                event.content.parts is not None and
                len(event.content.parts) > 0 and
                event.content.parts[0].text):
            text = event.content.parts[0].text
            print(text)
            final_output += text

    print("\n" + "=" * 60)
    print("SAVING TEAM ASSIGNMENTS TO MONGODB...")
    print("=" * 60)

    if final_output:
        parse_and_save_matches(final_output)

    print("=" * 60)
    print("MATCHING COMPLETE")


if __name__ == "__main__":
    asyncio.run(run_team_matcher())