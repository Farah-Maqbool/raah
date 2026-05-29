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

    async for event in runner.run_async(
    user_id="raah_user",
    session_id=session.id,
    new_message=content
    ):
        # Debug every single event
        author = getattr(event, 'author', 'NO_AUTHOR')
        has_content = event.content is not None
        has_text = (has_content and 
                    event.content.parts is not None and 
                    len(event.content.parts) > 0 and 
                    bool(event.content.parts[0].text))
        
        print(f"EVENT → author: '{author}' | has_content: {has_content} | has_text: {has_text}")
        
        if has_text:
            print(f"TEXT PREVIEW: {event.content.parts[0].text[:100]}")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run_raah_flow())