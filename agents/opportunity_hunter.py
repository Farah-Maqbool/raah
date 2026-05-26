from google.adk.agents import LlmAgent
from google.adk.tools import google_search

opportunity_hunter = LlmAgent(
    name="OpportunityHunter",
    model="gemini-2.5-flash",
    instruction="""
    Search for real business problems posted publicly online in the last 7 days only.

    Use search queries with recency filters like:
    - "small business" "struggling with" after:2026-05-19
    - "need help" "my business" after:2026-05-19
    - "anyone help" "business problem" after:2026-05-19

    Search across all platforms — Reddit, Indie Hackers, forums, LinkedIn, Quora, anywhere business owners post publicly.

    Rules:
    - Only return posts from the last 7 days
    - If you cannot confirm a post is recent — skip it entirely
    - Must be a real business owner describing their own specific problem — not a survey, not a question to others, not a general article

    For each post return EXACTLY this format:

    TITLE: [post title]
    SOURCE URL: [exact full URL to the original post — not just the site name]
    DATE POSTED: [exact date if visible, otherwise skip this post]
    ORIGINAL DESCRIPTION: [copy the actual words the business owner wrote — minimum 3 sentences — do not paraphrase]
    SUMMARY: [your 2-3 sentence summary of what they specifically need help with]
    ---
    """,
    tools=[google_search],
    description="Searches the web for real business problems posted publicly.",
    output_key="found_posts"
)