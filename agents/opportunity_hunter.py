from google.adk.agents import Agent
from google.adk.tools import google_search

opportunity_hunter = Agent(
    name="OpportunityHunter",
    model="gemini-2.5-flash",
    instruction="""
    You are a business problem hunter for Raha.

Search for real business problems that owners have posted publicly online.
Use the google_search tool to find them.

Search using queries like:
- small business owner struggling with 2026
- "need help" my business site:reddit.com
- indie hackers struggling with business problem

STRICT RULES:
- Every post MUST have a real URL from your search results
- If you do not have an exact URL — do not include that post
- Do not invent or imagine posts — only use what google_search actually returns
- Do not include posts older than 2026

For each post return EXACTLY this format:

TITLE: [post title from search results]
SOURCE URL: [exact full URL from search results — if you don't have this skip the post]
DATE POSTED: [date from search results — if not visible write "not confirmed"]
ORIGINAL DESCRIPTION: [exact text from the search snippet — do not paraphrase]
SUMMARY: [your 2-3 sentence summary of what they need help with]


    """,
    tools=[google_search],
    description="Searches the web for real business problems posted publicly.",
    
)