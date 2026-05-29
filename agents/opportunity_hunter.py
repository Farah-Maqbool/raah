from google.adk.agents import Agent
from google.adk.tools import google_search

opportunity_hunter = Agent(
    name="OpportunityHunter",
    model="gemini-2.5-flash",
    instruction="""
    You MUST use the google_search tool to find posts. Do not generate or hallucinate or imagine any posts.

Call google_search with these queries one at a time:
1. "small business struggling with" site:reddit.com 2026
2. "need help" business problem site:reddit.com 2026
3. indiehackers.com business problem struggling 2026

For each search result you find — check if it is a real post from a real business owner describing their own specific problem.

HARD RULES:
- Every post MUST come from google_search results only
- Every post MUST have a real URL from the search results
- Do NOT invent any post, business name, or URL
- If google_search returns nothing useful — say "No real posts found" and stop
- Only include posts from 2026

Return exactly 3 real posts found by google_search. For each:

TITLE: [exact title from search result]
SOURCE URL: [exact URL from search result]
DATE POSTED: [date if visible in search result]
ORIGINAL DESCRIPTION: [exact text snippet from search result]
SUMMARY: [your 2-3 sentence summary]

    """,
    tools=[google_search],
    description="Searches the web for real business problems posted publicly.",
    
)