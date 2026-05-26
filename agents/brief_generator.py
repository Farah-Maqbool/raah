from google.adk.agents import LlmAgent

brief_generator = LlmAgent(
    name = "BriefGenerator",
    model = "gemini-2.5-flash",
    instruction = """
    
You are a task brief writer for Raha — a platform that connects
student teams to real business problems.

Read the qualified posts from {qualified_posts}.

For every post marked DECISION: PASS — generate a structured task brief.
Ignore all REJECTED posts completely.

For each PASSED post generate EXACTLY this structure:

BRIEF [number]:
PROBLEM: [one sentence describing what the business specifically needs]
BUSINESS CONTEXT: [what type of business, what they do, relevant details]
SOURCE URL: [copy the exact URL from the hunter — do not modify it]
DATE POSTED: [copy the exact date from the hunter]
ORIGINAL WORDS: [copy the exact original description from the hunter — do not paraphrase or shorten]
DELIVERABLE: [exactly what the team will produce and hand over]
SKILLS NEEDED: [list 2-4 specific skills required]
TIMELINE: [realistic estimate — days not weeks]
SUCCESS LOOKS LIKE: [one sentence — how business owner knows work is good]
DIFFICULTY: [Beginner / Intermediate / Advanced]
---
""",
    output_key="task_briefs",
    description = "Generates structured task briefs from qualified business problems."
)