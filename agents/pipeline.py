import asyncio
from dotenv import load_dotenv
from google.adk import Workflow
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.opportunity_hunter import opportunity_hunter
from agents.qualifier import qualifier

load_dotenv()

raah_workflow = Workflow(
    name = "raah_flow",
    edges = [
        ("START", opportunity_hunter),
        (opportunity_hunter, qualifier)
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