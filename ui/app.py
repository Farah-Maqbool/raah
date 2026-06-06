import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

import streamlit as st
import asyncio
import threading
import queue

st.set_page_config(
    page_title="Raah — Real Work. Real Proof.",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid #1e1e1e !important;
}

[data-testid="stSidebar"] * { color: #e8e4dc !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #e8e4dc !important;
    padding: 8px 0 4px 0;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 24px;
}

.sidebar-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #4a4a4a !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 32px;
}

[data-testid="stRadio"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #6a6a6a !important;
    letter-spacing: 0.3px;
    padding: 6px 0 !important;
}

[data-testid="stRadio"] label:hover { color: #e8e4dc !important; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: #e8e4dc;
    letter-spacing: -1.5px;
    line-height: 1;
    margin: 0 0 6px 0;
}

.page-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #4a4a4a;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 40px;
}

.step-card {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-top: 2px solid #e8e4dc;
    padding: 28px 24px;
    height: 100%;
}

.step-number {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #4a4a4a;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #e8e4dc;
    margin-bottom: 10px;
}

.step-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #6a6a6a;
    line-height: 1.6;
}

.terminal {
    background: #0a0a0a;
    border: 1px solid #1e1e1e;
    border-top: 2px solid #e8e4dc;
    padding: 24px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #6a6a6a;
    min-height: 320px;
    max-height: 600px;
    overflow-y: auto;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}

.t-agent {
    color: #e8e4dc;
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 20px;
    margin-bottom: 4px;
    border-top: 1px solid #1e1e1e;
    padding-top: 16px;
}

.t-text { color: #6a6a6a; }
.t-success { color: #4a9463; }
.t-dim { color: #3a3a3a; }

.stButton button {
    background: #e8e4dc !important;
    color: #0a0a0a !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 12px 32px !important;
    font-weight: 500 !important;
}

.stButton button:hover { background: #ffffff !important; }

hr { border-color: #1e1e1e !important; margin: 32px 0 !important; }

[data-testid="stMetric"] {
    background: #111111;
    border: 1px solid #1e1e1e;
    padding: 20px !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 40px !important;
    font-weight: 800 !important;
    color: #e8e4dc !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    color: #4a4a4a !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

.stTextInput input {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 0 !important;
}

.stCheckbox label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #9a9a9a !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 0 !important;
    color: #e8e4dc !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Raah</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Real Work. Real Proof.</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["Home", "Run Agent", "Team Matches", "Add Profile"],
        label_visibility="collapsed"
    )

    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family: DM Mono, monospace; font-size: 10px; color: #2a2a2a; letter-spacing: 1px;">GOOGLE CLOUD HACKATHON 2026</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────
# PAGE 1 — HOME
# ─────────────────────────────────────────
if page == "Home":

    st.markdown('<div class="page-title">Break the loop.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Graduate unemployment and beyond</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div style="font-family: DM Sans, sans-serif; font-size: 17px; color: #9a9a9a; line-height: 1.8; max-width: 520px;">
        Thousands of graduates leave university every year with real skills
        and zero proof of them. Every job requires experience.
        Every experience requires a job. Nobody breaks the loop.
        <br><br>
        Raah does not connect graduates to jobs. It gives them real work
        before anyone will hire them — so the loop breaks before it starts.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #0f0f0f; border: 1px solid #1e1e1e; border-left: 2px solid #e8e4dc; padding: 24px;">
        <div style="font-family: DM Mono, monospace; font-size: 10px; color: #4a4a4a; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;">Survey — 15 Pakistani Graduates</div>
        <div style="font-family: Syne, sans-serif; font-size: 42px; font-weight: 800; color: #e8e4dc; letter-spacing: -2px; line-height: 1;">80%</div>
        <div style="font-family: DM Sans, sans-serif; font-size: 13px; color: #6a6a6a; margin-bottom: 20px;">cited the experience trap as their primary barrier</div>
        <div style="font-family: Syne, sans-serif; font-size: 42px; font-weight: 800; color: #e8e4dc; letter-spacing: -2px; line-height: 1;">93%</div>
        <div style="font-family: DM Sans, sans-serif; font-size: 13px; color: #6a6a6a;">would try a team-based real-work solution</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-family: DM Mono, monospace; font-size: 10px; color: #4a4a4a; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 24px;">How It Works</div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("01", "Agent Hunts", "Scans Reddit, Indie Hackers, and public forums for real business problems posted by real owners."),
        ("02", "Agent Qualifies", "Reasons through each post — is it real, specific, bounded, solvable by outsiders? Only real problems pass."),
        ("03", "Team Matched", "Graduates matched to the right problem based on skills. No bidding. No competition. The agent assigns."),
        ("04", "Work Verified", "Business confirms delivery. A permanent verified record is added — not a certificate. Proof of real work.")
    ]
    for col, (num, title, body) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-number">{num}</div>
                <div class="step-title">{title}</div>
                <div class="step-body">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    try:
        from database.opportunities import get_open_briefs
        from database.profiles import get_available_profile
        briefs = get_open_briefs()
        profiles = get_available_profile()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Open Briefs", len(briefs))
        with c2:
            st.metric("Available Graduates", len(profiles))
        with c3:
            st.metric("Projects Completed", 0)
    except Exception:
        pass


# ─────────────────────────────────────────
# PAGE 2 — RUN AGENT
# ─────────────────────────────────────────
elif page == "Run Agent":

    st.markdown('<div class="page-title">Run the Agent.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Live pipeline — each agent output appears as it runs</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family: DM Mono, monospace; font-size: 11px; color: #4a4a4a; line-height: 2.2; border: 1px solid #1e1e1e; padding: 20px; margin-bottom: 32px;">
    PIPELINE &nbsp;&nbsp;/&nbsp; OpportunityHunter &rarr; Qualifier &rarr; BriefGenerator &rarr; MongoDB<br>
    MODEL &nbsp;&nbsp;&nbsp;&nbsp;/&nbsp; Gemini 2.5 Flash (search) + Groq Llama 3.3 70B (reasoning)<br>
    FRAMEWORK&nbsp;/&nbsp; Google ADK 2.0 Workflow<br>
    DATABASE &nbsp;/&nbsp; MongoDB Atlas
    </div>
    """, unsafe_allow_html=True)

    run_clicked = st.button("Run Pipeline", type="primary")

    terminal = st.empty()

    def render_terminal(lines):
        html = '<div class="terminal">'
        for text, cls in lines:
            html += f'<div class="{cls}">{text}</div>'
        html += '</div>'
        terminal.markdown(html, unsafe_allow_html=True)

    if run_clicked:
        log = []

        def add(text, cls="t-text"):
            log.append((text, cls))
            render_terminal(log)

        add("RAHA PIPELINE STARTING", "t-agent")
        add("Initializing session and workflow...")

        output_queue = queue.Queue()
        error_holder = {"error": ""}

        def stream_pipeline():
            import io

            class QueueWriter(io.TextIOBase):
                def write(self, s):
                    if s.strip():
                        output_queue.put(s.strip())
                    return len(s)

            try:
                import sys as _sys
                old_stdout = _sys.stdout
                _sys.stdout = QueueWriter()

                from agents.workflow import run_raah_flow
                asyncio.run(run_raah_flow())

                _sys.stdout = old_stdout
                output_queue.put("__DONE__")

            except Exception as e:
                output_queue.put(f"__ERROR__{str(e)}")

        thread = threading.Thread(target=stream_pipeline)
        thread.start()

        add("OPPORTUNITY HUNTER", "t-agent")
        add("Searching for real business problems across Reddit and Indie Hackers...")

        current_agent = "hunter"

        while True:
            try:
                msg = output_queue.get(timeout=120)

                if msg == "__DONE__":
                    add("PIPELINE COMPLETE", "t-agent")
                    add("New briefs saved to MongoDB.", "t-success")
                    add("Duplicates automatically skipped.", "t-dim")
                    break

                elif msg.startswith("__ERROR__"):
                    err = msg.replace("__ERROR__", "")
                    add("PIPELINE ERROR", "t-agent")
                    add(err, "t-text")
                    break

                else:
                    # Detect agent transitions from printed output
                    if "AGENT: Qualifier" in msg or "qualifier" in msg.lower() and current_agent != "qualifier":
                        current_agent = "qualifier"
                        add("QUALIFIER", "t-agent")
                        add("Reasoning through each post — real, specific, bounded, solvable?")

                    elif "AGENT: BriefGenerator" in msg or "brief" in msg.lower() and current_agent not in ["brief", "qualifier"]:
                        if current_agent == "qualifier":
                            current_agent = "brief"
                            add("BRIEF GENERATOR", "t-agent")
                            add("Generating structured task briefs for passed posts...")

                    elif "SAVING" in msg:
                        add("MONGODB", "t-agent")
                        add("Parsing and saving briefs...")

                    elif "Saved:" in msg:
                        add(msg, "t-success")

                    elif "Skipped" in msg or "duplicate" in msg.lower():
                        add(msg, "t-dim")

                    else:
                        # Show first 120 chars of any other output
                        clean = msg[:120] + ("..." if len(msg) > 120 else "")
                        add(clean)

            except queue.Empty:
                add("Timeout — pipeline took too long.", "t-text")
                break

        thread.join()

    else:
        render_terminal([
            ("WAITING FOR TRIGGER", "t-agent"),
            ("Press Run Pipeline to start.", "t-dim"),
            ("", "t-dim"),
            ("The agent will search for real business problems,", "t-dim"),
            ("qualify each one through multi-step reasoning,", "t-dim"),
            ("generate structured task briefs,", "t-dim"),
            ("and save new briefs to MongoDB automatically.", "t-dim"),
        ])


# ─────────────────────────────────────────
# PAGE 3 — TEAM MATCHES
# ─────────────────────────────────────────
elif page == "Team Matches":

    st.markdown('<div class="page-title">Team Matches.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Graduates matched to real business problems by the agent</div>', unsafe_allow_html=True)

    try:
        from database.opportunities import get_open_briefs
        from database.profiles import get_available_profile

        briefs = get_open_briefs()
        profiles = get_available_profile()

        if not briefs:
            st.markdown("""
            <div style="border: 1px solid #1e1e1e; padding: 40px; text-align: center;
            font-family: DM Mono, monospace; font-size: 12px; color: #4a4a4a; letter-spacing: 1px;">
            No open briefs yet. Run the agent first.
            </div>
            """, unsafe_allow_html=True)

        elif not profiles:
            st.markdown("""
            <div style="border: 1px solid #1e1e1e; padding: 40px; text-align: center;
            font-family: DM Mono, monospace; font-size: 12px; color: #4a4a4a; letter-spacing: 1px;">
            No graduate profiles yet. Add profiles first.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="font-family: DM Mono, monospace; font-size: 10px; color: #4a4a4a;
            letter-spacing: 1.5px; margin-bottom: 24px;">
            {len(briefs)} BRIEFS — {len(profiles)} GRADUATES — MATCHED BY SKILLS
            </div>
            """, unsafe_allow_html=True)

            for i, brief in enumerate(briefs):
                skills_needed = brief.get("skills_needed", [])

                # Match profiles to brief
                matched = []
                for profile in profiles:
                    profile_skills = profile.get("skills", [])
                    overlap = [
                        s for s in skills_needed
                        if any(s.lower() in ps.lower() for ps in profile_skills)
                    ]
                    if overlap:
                        matched.append((profile, overlap))

                matched.sort(key=lambda x: len(x[1]), reverse=True)
                top_team = matched[:3]

                # Brief header
                st.markdown(f"""
                <div style="background: #0f0f0f; border: 1px solid #1e1e1e;
                border-left: 2px solid #e8e4dc; padding: 20px 24px; margin-bottom: 8px;">
                    <div style="font-family: DM Mono, monospace; font-size: 10px;
                    color: #4a4a4a; letter-spacing: 1.5px; margin-bottom: 8px;">
                    BRIEF {i+1:02d}
                    </div>
                    <div style="font-family: Syne, sans-serif; font-size: 16px;
                    font-weight: 700; color: #e8e4dc; margin-bottom: 8px;">
                    {brief.get("problem", "N/A")}
                    </div>
                    <div style="font-family: DM Sans, sans-serif; font-size: 12px; color: #6a6a6a;">
                    Skills needed: {", ".join(skills_needed)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Team cards
                if top_team:
                    tcols = st.columns(len(top_team))
                    for j, (profile, overlap) in enumerate(top_team):
                        with tcols[j]:
                            overlap_tags = "".join([
                                f'<span style="display:inline-block; background:#1a1a1a; border:1px solid #2a2a2a; color:#6a6a6a; font-family:DM Mono,monospace; font-size:10px; padding:3px 8px; margin:2px 2px 2px 0;">{s}</span>'
                                for s in overlap
                            ])
                            st.markdown(f"""
                            <div style="background: #111111; border: 1px solid #1e1e1e;
                            padding: 18px; margin-bottom: 24px;">
                                <div style="font-family: Syne, sans-serif; font-size: 15px;
                                font-weight: 700; color: #e8e4dc; margin-bottom: 2px;">
                                {profile.get("name", "Unknown")}
                                </div>
                                <div style="font-family: DM Mono, monospace; font-size: 10px;
                                color: #4a4a4a; letter-spacing: 0.5px; margin-bottom: 12px;">
                                {profile.get("field", "")} — {profile.get("university", "")}
                                </div>
                                <div style="font-family: DM Mono, monospace; font-size: 10px;
                                color: #4a4a4a; letter-spacing: 1px; margin-bottom: 6px;">
                                MATCHING SKILLS
                                </div>
                                {overlap_tags}
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="font-family: DM Mono, monospace; font-size: 11px;
                    color: #3a3a3a; padding: 12px 0 24px 0;">
                    No matching graduates found for this brief.
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")


# ─────────────────────────────────────────
# PAGE 4 — ADD PROFILE
# ─────────────────────────────────────────
elif page == "Add Profile":

    st.markdown('<div class="page-title">Join Raah.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Share your skills — get matched to real work</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family: DM Sans, sans-serif; font-size: 14px; color: #6a6a6a; line-height: 1.8; max-width: 480px; margin-bottom: 32px;">
    You do not need experience to join. That is the point.
    Tell us what you can do and the agent will find work that fits.
    When you deliver — you get a verified record. Not a certificate. Real proof.
    </div>
    """, unsafe_allow_html=True)

    with st.form("profile_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            university = st.text_input("University")

        with col2:
            field = st.selectbox(
                "Field of Study",
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

        st.markdown("""
        <div style="font-family: DM Mono, monospace; font-size: 10px; color: #4a4a4a; letter-spacing: 1.5px; text-transform: uppercase; margin: 24px 0 12px 0;">
        Select Your Skills
        </div>
        """, unsafe_allow_html=True)

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
                if st.checkbox(skill, key=f"skill_{i}"):
                    selected_skills.append(skill)

        other_skills = st.text_input("Other skills — comma separated")

        st.markdown("<br>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Join Raah", type="primary")

        if submitted:
            if not name or not email:
                st.error("Name and email are required.")
            elif not selected_skills and not other_skills:
                st.error("Select at least one skill.")
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

                try:
                    from database.profiles import save_profile
                    success = save_profile(profile)
                    if success:
                        st.success(f"Welcome, {name}. You are now in the system. The agent will match you to a real problem soon.")
                    else:
                        st.warning("An account with this email already exists.")
                except Exception as e:
                    st.error(f"Error saving profile: {e}")