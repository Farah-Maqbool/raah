import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_briefs(raw_text: str) -> list:
    briefs = []
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
                brief["problem"] = line.replace("PROBLEM:", "").strip()

            elif line.startswith("BUSINESS CONTEXT:"):
                brief["business_context"] = line.replace("BUSINESS CONTEXT:", "").strip()

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
PROBLEM: Test problem here.
BUSINESS CONTEXT: Small e-commerce store.
SOURCE URL: https://reddit.com/r/smallbusiness/test
DATE POSTED: May 2026
ORIGINAL WORDS: We are struggling with customer retention.
DELIVERABLE: A strategy report.
SKILLS NEEDED: Marketing, Research
TIMELINE: 7 days
SUCCESS LOOKS LIKE: Owner has clear action plan.
DIFFICULTY: Intermediate
---
    """
    briefs = parse_briefs(test_output)
    print(f"Parsed {len(briefs)} briefs")
    for b in briefs:
        print(b)