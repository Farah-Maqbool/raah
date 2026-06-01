import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.genai import types
from database.opportunities import get_open_briefs
from database.profiles import get_available_profile

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
    profiles = get_available_profile()
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

team_matcher = Agent(
    name="team_matcher",
    model = LiteLlm(model="groq/llama-3.3-70b-versatile"),
    instruction="""
You are TeamMatcher — an agent inside Raha that matches real business 
problems to the right student teams.

YOUR JOB:
1. Use get_open_briefs_tool to get all open business problems
2. Use get_available_profiles_tool to get all available graduates
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

    async for event in runner.run_async(
        user_id="matcher_user",
        session_id=session.id,
        new_message=content
    ):
        if (event.content is not None and
                event.content.parts is not None and
                len(event.content.parts) > 0 and
                event.content.parts[0].text):
            print(event.content.parts[0].text)

    print("\n" + "=" * 60)
    print("MATCHING COMPLETE")


if __name__ == "__main__":
    asyncio.run(run_team_matcher())

