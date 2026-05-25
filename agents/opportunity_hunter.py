from google.adk.agents import LlmAgent
from google.adk.tools import google_search

opportunity_hunter = LlmAgent(
    name="OpportunityHunter",
    model="gemini-2.5-flash",
    instruction="""
    Search for real business problems people have posted publicly online.
    Search sites like indiehackers.com and reddit.com/r/smallbusiness.
    Find posts where a real business owner describes a specific problem 
    they are stuck on.
    Return exactly 5 posts. For each post return:
    TITLE: [post title]
    SOURCE: [url or site name]
    SUMMARY: [2-3 sentence summary of the specific problem described]
    ---
    """,
    tools=[google_search],
    description="Searches the web for real business problems posted publicly.",
    output_key="found_posts"
)