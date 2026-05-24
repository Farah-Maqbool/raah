import asyncio
import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

opportunity_hunter = Agent(
    name = "Opportunity_Hunter",
    model = "gemini-2.5-flash",
    tools = [google_search],
    description = """Search for real business problems people have posted publicly online.
    Search sites like indiehackers.com, reddit.com/r/smallbusiness, and similar forums.
    Find posts where a real business owner describes a specific problem they are stuck on.
    Return the post title, source, and a summary of the problem described."""
)

async def run_agent(query: str):
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        state = {},
        app_name = "raha",
        user_id = "test_user"
    )

    runner = Runner(
        app_name = "raha",
        agent = opportunity_hunter,
        session_service  = session_service
    )

    content = types.Content(
        role = "user",
        parts = [types.Part(text=query)]
    )

    async for event in runner.run_async(
        user_id= "test_user",
        session_id = session.id,
        new_message = content
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(run_agent(
        "Find 3 recent posts where small business owners describe a specific problem they need help solving"
    ))
    