import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_briefs(raw_text: str) -> list:
    """
    Parse raw brief generator output into structured dicts for MongoDB.
    """
    
    briefs = []

    #split by brief marker
    sections = raw_text.split("BRIEF")

    for section in sections:
        if not section.strip():
            continue

        if "PROBLEM:" not in section:
            continue

        brief = {}

        lines = section.strip().split("\n")

        for line in lines:
            line = line.strip()

            if line.startswith("PROBLEM:"):
                brief["problem"] = line.replace("PROBLEM:","").strip()

            elif line.startswith("BUSINESS CONTEXT:"):
                brief["business_context"] = line.replace("BUSINESS CONTEXT:","").strip

            elif line.startswith("SOURCE URL:"):
                brief["source_url"] = line.replace("SOURCE URL:", "").strip()
            
            elif line.startswith("DATE POSTED:"):
                brief["date_posted"] = line.replace("DATE POSTED:", "").strip()
            
            elif line.startswith("ORIGINAL WORDS:"):
                brief["original_words"] = line.replace("ORIGINAL WORDS:", "").strip()
            
            elif line.startswith("DELIVERABLE:"):
                brief["deliverable"] = line.replace("DELIVERABLE:", "").strip()
            
            elif line.startswith("SKILLS NEEDED:"):
                skills_raw = line.replace("SKILLS NEEDED:", "").strip()
                brief["skills_needed"] = [s.strip() for s in skills_raw.split(",")]
            
            elif line.startswith("TIMELINE:"):
                brief["timeline"] = line.replace("TIMELINE:", "").strip()
            
            elif line.startswith("SUCCESS LOOKS LIKE:"):
                brief["success_looks_like"] = line.replace("SUCCESS LOOKS LIKE:", "").strip()
            
            elif line.startswith("DIFFICULTY:"):
                brief["difficulty"] = line.replace("DIFFICULTY:", "").strip()

        if brief.get("problem") and brief.get("source_url"):
            briefs.append(brief)
    
    return briefs

if __name__ == "__main__":
    test_output = """
    BRIEF 1:
    PROBLEM: An indie hacker needs to shift focus from feature building to marketing.
    BUSINESS CONTEXT: Solo founder of Karmo, a Reddit Marketing Tool.
    SOURCE URL: https://reddit.com/r/indiehackers/test
    DATE POSTED: May 21 2026
    ORIGINAL WORDS: I keep building features instead of marketing my product.
    DELIVERABLE: A prioritized marketing strategy and action plan.
    SKILLS NEEDED: Marketing Strategy, Market Research, Growth Hacking
    TIMELINE: 7-10 days
    SUCCESS LOOKS LIKE: Owner has a clear plan to acquire users.
    DIFFICULTY: Intermediate
    """

    briefs = parse_briefs(test_output)
    print(f"Parsed {len(briefs)} briefs")

    for b in briefs:
        print(b)

