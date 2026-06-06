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
from database.teams import assign_team, get_team_by_brief

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
    Extracts brief_id and team member emails from the output.
    """
    briefs = get_open_briefs()
    brief_lookup = {b.get("problem", "").lower()[:40]: b.get("source_url") for b in briefs}

    # Split by MATCH blocks
    blocks = re.split(r"MATCH\s+\d+:", raw_output)

    saved = 0
    for block in blocks:
        if not block.strip():
            continue

        # Extract brief problem to find source_url
        brief_match = re.search(r"BRIEF:\s*(.+)", block)
        if not brief_match:
            continue

        brief_problem = brief_match.group(1).strip().lower()[:40]

        # Find source_url by matching problem text
        source_url = None
        for key, url in brief_lookup.items():
            if key[:30] in brief_problem[:30] or brief_problem[:30] in key[:30]:
                source_url = url
                break

        if not source_url:
            # Try to find BRIEF_ID directly if agent included it
            id_match = re.search(r"BRIEF_ID:\s*(.+)", block)
            if id_match:
                source_url = id_match.group(1).strip()

        if not source_url:
            print(f"Could not find source URL for block — skipping")
            continue

        # Check if team already assigned
        existing = get_team_by_brief(source_url)
        if existing:
            print(f"Team already assigned for this brief — skipping")
            continue

        # Extract emails from team lines
        # Format: - Name | email@example.com | skills
        email_pattern = re.findall(r"\|\s*([\w.+-]+@[\w.-]+\.\w+)\s*\|", block)

        if not email_pattern:
            print(f"No emails found in match block — skipping")
            continue

        # Save to MongoDB
        success = assign_team(source_url, email_pattern)
        if success:
            print(f"Team saved: {email_pattern} → {source_url[:50]}")
            saved += 1
        else:
            print(f"Failed to save team for {source_url[:50]}")

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
3. For each brief — find 2 to 3 graduates whose skills match best
4. Form a team for each brief

MATCHING RULES:
- Match skills needed in the brief to skills listed in profiles
- A team should have complementary skills — not all the same
- Pick 2 to 3 people per brief maximum
- Each person can only be in one team at a time
- If no good match exists for a brief — say "No match found" for that brief

OUTPUT FORMAT:
For each brief produce exactly this:

MATCH [number]:
BRIEF: [problem statement]
BRIEF_ID: [copy the BRIEF_ID exactly from the brief data]
SKILLS NEEDED: [skills from brief]
TEAM:
  - [Name] | [Email] | [Matching skills]
  - [Name] | [Email] | [Matching skills]
REASON: [one sentence explaining why this team fits this brief]
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