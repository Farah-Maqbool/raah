import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from dotenv import load_dotenv
from google.adk import Workflow
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.opportunity_hunter import opportunity_hunter
from agents.qualifier import qualifier
from agents.brief_generator import brief_generator
from database.brief_parser import parse_briefs
from database.opportunities import save_brief

load_dotenv()

raah_workflow = Workflow(
    name = "raah_flow",
    edges = [
        ("START", opportunity_hunter, qualifier, brief_generator)
    ]
)

async def run_raah_flow():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        state = {},
        app_name = "raah",
        user_id= "raah_user"
    )

    runner = Runner(
        app_name = "raah",
        agent = raah_workflow,
        session_service=session_service
    )

    content = types.Content(
        role = "user",
        parts = [
            types.Part(text="Find and qualify 3 real business problems for student teams to solve.")
        ]
    )

    print("\nRAAH PIPELINE STARTING...\n")
    print("=" * 60)

    final_output = ""

    async for event in runner.run_async(
    user_id="raah_user",
    session_id=session.id,
    new_message=content
    ):
        
        author = getattr(event, "author")
        has_text = (
            event.content is not None and 
            event.content.parts is not None and
            len(event.content.parts) > 0 and
            bool(event.content.parts[0].text)
        )

        if has_text:
            text = event.content.parts[0].text

            print(f"\n{'=' * 60}")
            print(f"AGENT: {author}")
            print(f"{'=' * 60}\n")
            print(text)

            if author=="BriefGenerator":
                final_output = text
    
    print(f"\n{'=' * 60}")
    print("SAVING TO MONGODB...")
    print("=" * 60)

    if final_output:
        briefs = parse_briefs(final_output)

        saved = 0
        skipped = 0

        for brief in briefs:
            if save_brief(brief):
                saved += 1
            else:
                skipped += 1
            
        print(f"Saved: {saved} new briefs")
        print(f"Skipped: {skipped} duplicates")
    else:
        print("No briefs")



if __name__ == "__main__":
    asyncio.run(run_raah_flow())