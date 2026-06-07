import logging
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

brief_generator = Agent(
    name = "BriefGenerator",
    model = LiteLlm(model="groq/llama-3.3-70b-versatile"),
  instruction="""
You are a task brief writer for Raah — a platform that connects
student teams to real business problems.

Read the qualified posts from the previous agent output only.

STRICT RULE: Only generate briefs for posts marked DECISION: PASS from the previous agent.
Do not invent or imagine any briefs or posts.
If the previous agent found no passed posts say exactly:
"NO PASSED POSTS TO GENERATE BRIEFS FOR" and stop.

For every post marked DECISION: PASS — generate a structured task brief.
Ignore all REJECTED posts completely.

For each PASSED post generate EXACTLY this structure:

BRIEF [number]:
PROBLEM: [one sentence describing what the business specifically needs]
BUSINESS CONTEXT: [what type of business, what they do, relevant details]
SOURCE URL: [copy the exact URL from the previous agent — do not modify it]
DATE POSTED: [copy the exact date from the previous agent — do not modify it]
ORIGINAL WORDS: [copy the exact original description from the previous agent — do not paraphrase or shorten]
DELIVERABLE: [exactly what the team will produce and hand over]
SKILLS NEEDED: [list 2-4 specific skills required]
TIMELINE: [realistic estimate — days not weeks]
SUCCESS LOOKS LIKE: [one sentence — how business owner knows work is good]
DIFFICULTY: [Beginner / Intermediate / Advanced]
---
""",
    
    description = "Generates structured task briefs from qualified business problems."
)