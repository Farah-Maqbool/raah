import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

import streamlit as st
import asyncio
from database.opportunities import get_open_briefs
from database.profiles import get_available_profile

st.set_page_config(
    page_title="Raah",
    layout="wide"
)

#sidebar

with st.sidebar:
    st.markdown(" ### Navigation")
    page = st.radio(
        "",
        ["Home","Run Agent","Open Briefs","Team Matches", "Join as Graduate"],
        label_visibility='collapsed'
    )

# page 1

if page == "Home":
    st.markdown("# Raha")

    st.markdown("### Real business problems. Real student teams. Real portfolios.")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("**The Problem**")
        st.write(
            "80% of Pakistani graduates say the experience trap is "
            "their biggest barrier. No experience to get a job. "
            "No job to get experience."
        )
    with col2:
        st.warning("**Existing Solutions Failed**")
        st.write(
            "Job boards, internship platforms, online courses — "
            "they all require experience you already don't have. "
            "Certificates nobody trusts."
        )
    with col3:
        st.success("**What Raha Does**")
        st.write(
            "An AI agent finds real unsolved business problems, "
            "matches them to student teams, and verifies the work. "
            "No bidding. No fake projects. Real proof."
        )

    st.divider()

    st.markdown("## How It Works")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**1. Agent Hunts**")
        st.write("Scans Reddit, Indie Hackers, and forums for real business problems posted publicly.")
    with c2:
        st.markdown("**2. Agent Qualifies**")
        st.write("Reasons through each post is it real, specific, bounded, solvable by outsiders?")
    with c3:
        st.markdown("**3. Team Matched**")
        st.write("Right graduates matched to right problem based on skills. No bidding war.")
    with c4:
        st.markdown("**4. Work Verified**")
        st.write("Business confirms delivery. Permanent verified record added to portfolio.")

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        briefs = get_open_briefs()
        st.metric("Open Briefs", len(briefs))
    with col2:
        profiles = get_available_profile()
        st.metric("Available Graduates", len(profiles))
    with col3:
        st.metric("Projects Completed", 0)


# page 2

elif page == "Run Agent":
    st.markdown("# Raah Agent")
    st.markdown("Watch the agent find and qualify real business problems in real time.")
    st.divider()

    st.info("""
    **What happens when you run:**
    - Agent searches Reddit and Indie Hackers for real business problems
    - Qualifies each post through multi-step reasoning
    - Generates structured task briefs
    - Saves new briefs to database automatically
    """)

    if st.button("Run Agent Now", type="primary", use_container_width=True):

        with st.status("Agent running...", expanded=True) as status:

            st.write("OpportunityHunter searching for real business problems...")

            output_container = st.empty()

            try:
                import subprocess
                import threading

                result_holder = {"output": "", "error": ""}

                def run_pipeline():
                    try:
                        from agents.workflow import run_raah_flow
                        asyncio.run(run_raah_flow())
                        result_holder["output"] = "done"
                    except Exception as e:
                        result_holder["error"] = str(e)

                thread = threading.Thread(target=run_pipeline)
                thread.start()
                thread.join()

                if result_holder["error"]:
                    status.update(label="Agent failed", state="error")
                    st.error(result_holder["error"])
                else:
                    status.update(label="Agent complete", state="complete")
                    st.success("Pipeline finished. New briefs saved to database.")
                    st.balloons()

            except Exception as e:
                status.update(label="Error", state="error")
                st.error(str(e))

elif page == "Open Briefs":
    st.markdown("# 📋 Open Business Problems")
    st.markdown("Real problems found by the Raha agent — ready for student teams.")
    st.divider()

    briefs = get_open_briefs()

    if not briefs:
        st.info("No open briefs yet. Run the agent to find real business problems.")
    else:
        st.success(f"{len(briefs)} real business problems available")

        for i, brief in enumerate(briefs):
            with st.expander(
                f"**Brief {i+1}** — {brief.get('problem', '')[:80]}...",
                expanded=(i == 0)
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("**Problem**")
                    st.write(brief.get("problem", "N/A"))

                    st.markdown("**Business Context**")
                    st.write(brief.get("business_context", "N/A"))

                    st.markdown("**Deliverable**")
                    st.write(brief.get("deliverable", "N/A"))

                    st.markdown("**Original Words From Business Owner**")
                    st.info(f'"{brief.get("original_words", "N/A")}"')

                with col2:
                    st.markdown("**Skills Needed**")
                    for skill in brief.get("skills_needed", []):
                        st.markdown(f"• {skill}")

                    st.markdown("**Difficulty**")
                    difficulty = brief.get("difficulty", "N/A")
                    if difficulty == "Beginner":
                        st.success(difficulty)
                    elif difficulty == "Intermediate":
                        st.warning(difficulty)
                    else:
                        st.error(difficulty)

                    st.markdown("**Timeline**")
                    st.write(brief.get("timeline", "N/A"))

                    st.markdown("**Date Posted**")
                    st.write(brief.get("date_posted", "N/A"))

                    st.markdown("**Source**")
                    url = brief.get("source_url", "")
                    if url.startswith("http"):
                        st.markdown(f"[View Original Post]({url})")
                    else:
                        st.write(url)

elif page == "Team Matches":
    st.markdown("# 👥 Team Matches")
    st.markdown("Graduates matched to real business problems by the Raha agent.")
    st.divider()

    briefs = get_open_briefs()
    profiles = get_available_profile()

    if not briefs:
        st.info("No open briefs yet. Run the agent first.")
    elif not profiles:
        st.info("No graduate profiles yet.")
    else:
        if st.button("🤖 Match Teams Now", type="primary"):
            with st.spinner("Matching teams..."):
                try:
                    from agents.team_matcher import run_team_matcher
                    asyncio.run(run_team_matcher())
                    st.success("Matching complete.")
                except Exception as e:
                    st.error(str(e))

        st.divider()

        for i, brief in enumerate(briefs):
            st.markdown(f"### Brief {i+1}")
            st.write(brief.get("problem", ""))

            skills_needed = brief.get("skills_needed", [])
            st.markdown("**Skills needed:** " + ", ".join(skills_needed))

            matched = []
            for profile in profiles:
                profile_skills = profile.get("skills", [])
                overlap = [s for s in skills_needed
                          if any(s.lower() in ps.lower()
                          for ps in profile_skills)]
                if overlap:
                    matched.append((profile, overlap))

            matched.sort(key=lambda x: len(x[1]), reverse=True)
            top_team = matched[:3]

            if top_team:
                st.markdown("**Matched Team:**")
                cols = st.columns(len(top_team))
                for j, (profile, overlap) in enumerate(top_team):
                    with cols[j]:
                        with st.container(border=True):
                            st.markdown(f"**{profile.get('name')}**")
                            st.caption(profile.get("field", ""))
                            st.caption(profile.get("university", ""))
                            st.markdown("Matching skills:")
                            for skill in overlap:
                                st.markdown(f"• {skill}")
            else:
                st.warning("No matching graduates found for this brief.")

            st.divider()


# ─────────────────────────────────────────
# PAGE 5 — JOIN AS GRADUATE
# ─────────────────────────────────────────
elif page == "Join as Graduate":
    st.markdown("# Join Raah as a Graduate")
    st.markdown("Tell us your skills and we will match you to real business problems.")
    st.divider()

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            university = st.text_input("University")

        with col2:
            field = st.selectbox(
                "Field of Study *",
                [
                    "Computer Science / AI",
                    "Business / Marketing",
                    "Finance / Accounting",
                    "Design / Media",
                    "Engineering",
                    "Social Sciences",
                    "Other"
                ]
            )
            level = st.selectbox(
                "Level",
                ["Undergraduate", "Graduate", "Recent Graduate"]
            )

        st.markdown("**Your Skills** — select all that apply")

        skill_options = [
            "Python", "Machine Learning", "Data Analysis",
            "Marketing Strategy", "Social Media", "Content Creation",
            "Market Research", "UI/UX Design", "Figma",
            "Financial Modeling", "Excel", "Research",
            "B2B Sales", "Business Strategy", "Communication",
            "Web Development", "Graphic Design", "Video Editing",
            "SEO", "Copywriting", "Project Management"
        ]

        cols = st.columns(3)
        selected_skills = []
        for i, skill in enumerate(skill_options):
            with cols[i % 3]:
                if st.checkbox(skill):
                    selected_skills.append(skill)

        other_skills = st.text_input(
            "Other skills not listed above (comma separated)"
        )

        submitted = st.form_submit_button(
            "Join Raha",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not name or not email:
                st.error("Name and email are required.")
            elif not selected_skills and not other_skills:
                st.error("Please select at least one skill.")
            else:
                if other_skills:
                    extra = [s.strip() for s in other_skills.split(",") if s.strip()]
                    selected_skills.extend(extra)

                profile = {
                    "name": name,
                    "email": email,
                    "university": university,
                    "field": field,
                    "level": level,
                    "skills": selected_skills
                }

                from database.profiles import save_profile
                success = save_profile(profile)

                if success:
                    st.success(f"Welcome to Raha, {name}! You will be matched to a real business problem soon.")
                    st.balloons()
                else:
                    st.warning("An account with this email already exists.")
