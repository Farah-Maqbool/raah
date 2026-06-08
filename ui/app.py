import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

import streamlit as st
import asyncio
import threading
import queue

# Session state init
if "user" not in st.session_state:
    st.session_state.user = None

st.set_page_config(
    page_title="Raah",
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

.chat-msg {
    padding: 10px 14px;
    margin-bottom: 8px;
    border: 1px solid #1e1e1e;
    background: #0f0f0f;
}

.chat-sender {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #4a4a4a;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

.chat-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #9a9a9a;
    line-height: 1.5;
}

.chat-mine {
    border-left: 2px solid #e8e4dc;
}

.status-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 10px;
    border: 1px solid #2a2a2a;
    color: #6a6a6a;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# AUTH — NOT LOGGED IN
# ─────────────────────────────────────────
if st.session_state.user is None:

    st.markdown('<div class="page-title">Raah.</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real Work. Real Proof.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        tab = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")

        if tab == "Login":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

                if submitted:
                    from database.auth import login_user
                    result = login_user(email, password)
                    if result["success"]:
                        st.session_state.user = result["user"]
                        st.rerun()
                    else:
                        st.error(result["message"])

        else:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                university = st.text_input("University")
                field = st.selectbox("Field", [
                    "Computer Science / AI", "Business / Marketing",
                    "Finance / Accounting", "Design / Media",
                    "Engineering", "Social Sciences", "Other"
                ])
                level = st.selectbox("Level", [
                    "Undergraduate", "Graduate", "Recent Graduate"
                ])

                st.markdown("""
                <div style="font-family: DM Mono, monospace; font-size: 10px;
                color: #4a4a4a; letter-spacing: 1.5px; margin: 16px 0 8px 0;">
                YOUR SKILLS
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
                        if st.checkbox(skill, key=f"su_skill_{i}"):
                            selected_skills.append(skill)

                other = st.text_input("Other skills — comma separated")
                submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

                if submitted:
                    if not name or not email or not password:
                        st.error("Name, email and password are required.")
                    elif not selected_skills and not other:
                        st.error("Select at least one skill.")
                    else:
                        if other:
                            selected_skills.extend([s.strip() for s in other.split(",") if s.strip()])
                        from database.auth import signup_user
                        result = signup_user(name, email, password, university, field, level, selected_skills)
                        if result["success"]:
                            st.success("Account created. Please login.")
                        else:
                            st.error(result["message"])

    with col2:
        st.markdown("""
        <div style="background: #0f0f0f; border: 1px solid #1e1e1e;
        border-left: 2px solid #e8e4dc; padding: 32px; margin-top: 48px;">
        <div style="font-family: DM Mono, monospace; font-size: 10px;
        color: #4a4a4a; letter-spacing: 1.5px; margin-bottom: 20px;">WHY RAAH</div>
        <div style="font-family: Syne, sans-serif; font-size: 36px; font-weight: 800;
        color: #e8e4dc; letter-spacing: -1px; line-height: 1.1; margin-bottom: 20px;">
        Real work.<br>Real proof.<br>No certificates.
        </div>
        <div style="font-family: DM Sans, sans-serif; font-size: 13px;
        color: #6a6a6a; line-height: 1.8;">
        The agent finds real business problems.<br>
        You get matched to one that fits your skills.<br>
        You solve it. Business confirms it.<br>
        That becomes your portfolio — verified, permanent, real.
        </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# LOGGED IN
# ─────────────────────────────────────────
else:
    user = st.session_state.user

    with st.sidebar:
        st.markdown('<div class="sidebar-brand">Raah</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="sidebar-tagline">{user["name"]}</div>',
            unsafe_allow_html=True
        )

        page = st.radio(
            "",
            ["Home", "My Brief", "Team Chat"],
            label_visibility="collapsed"
        )

        st.markdown("<br>" * 8, unsafe_allow_html=True)
        # st.markdown(
        #     '<div style="font-family: DM Mono, monospace; font-size: 10px; color: #2a2a2a; letter-spacing: 1px;">GOOGLE CLOUD HACKATHON 2026</div>',
        #     unsafe_allow_html=True
        # )

        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # ─────────────────────────────────────────
    # HOME
    # ─────────────────────────────────────────
    if page == "Home":

        st.markdown('<div class="page-title">Break the loop.</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Graduate unemployment — a global problem</div>', unsafe_allow_html=True)

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
            <div style="font-family: DM Mono, monospace; font-size: 10px; color: #4a4a4a; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;">Survey — 15 Graduates</div>
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
            from database.auth import get_all_users
            briefs = get_open_briefs()
            profiles = get_all_users()
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
    # MY BRIEF
    # ─────────────────────────────────────────
    elif page == "My Brief":

        st.markdown('<div class="page-title">My Brief.</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Your assigned business problem</div>', unsafe_allow_html=True)

        try:
            from database.opportunities import get_open_briefs
            from database.teams import get_teams_by_member, update_team_status

            user_email = user["email"]
            briefs = get_open_briefs()
            my_teams = get_teams_by_member(user_email)

            if not my_teams:
                st.markdown("""
                <div style="border: 1px solid #1e1e1e; padding: 40px; text-align: center;
                font-family: DM Mono, monospace; font-size: 12px; color: #4a4a4a;">
                No brief assigned yet. The agent is finding a problem that fits your skills.
                </div>
                """, unsafe_allow_html=True)

            else:
                for team in my_teams:
                    brief_url = team["brief_source_url"]
                    brief = next((b for b in briefs if b.get("source_url") == brief_url), None)

                    if not brief:
                        continue

                    status = team.get("status", "assigned")

                    st.markdown(f"""
                    <div style="background: #0f0f0f; border: 1px solid #1e1e1e;
                    border-left: 2px solid #e8e4dc; padding: 24px; margin-bottom: 16px;">
                        <div style="font-family: DM Mono, monospace; font-size: 10px;
                        color: #4a4a4a; letter-spacing: 1.5px; margin-bottom: 8px;">YOUR ACTIVE BRIEF</div>
                        <div style="font-family: Syne, sans-serif; font-size: 20px;
                        font-weight: 700; color: #e8e4dc; margin-bottom: 12px;">
                        {brief.get("problem", "N/A")}
                        </div>
                        <div style="font-family: DM Sans, sans-serif; font-size: 13px;
                        color: #6a6a6a; margin-bottom: 16px;">
                        {brief.get("deliverable", "N/A")}
                        </div>
                        <div style="font-family: DM Mono, monospace; font-size: 10px;
                        color: #4a4a4a;">TIMELINE: {brief.get("timeline", "N/A")} &nbsp;|&nbsp; DIFFICULTY: {brief.get("difficulty", "N/A")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f'<div class="status-badge">Status: {status.upper()}</div>', unsafe_allow_html=True)

                    st.markdown("""
                    <div style="font-family: DM Mono, monospace; font-size: 10px;
                    color: #4a4a4a; letter-spacing: 1.5px; margin-bottom: 8px;">ORIGINAL WORDS</div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="border-left: 2px solid #2a2a2a; padding: 12px 16px;
                    background: #0f0f0f; font-family: DM Mono, monospace; font-size: 12px;
                    color: #6a6a6a; line-height: 1.6; font-style: italic; margin-bottom: 24px;">
                    {brief.get("original_words", "N/A")}
                    </div>
                    """, unsafe_allow_html=True)

                    # Team members
                    members = team.get("members", [])
                    st.markdown(f"""
                    <div style="font-family: DM Mono, monospace; font-size: 10px;
                    color: #4a4a4a; letter-spacing: 1px; margin-bottom: 24px;">
                    TEAM: {" &nbsp;·&nbsp; ".join(members)}
                    </div>
                    """, unsafe_allow_html=True)

                    # WhatsApp group
                    from database.teams import save_whatsapp_link, get_whatsapp_link
                    existing_link = get_whatsapp_link(brief_url)

                    if existing_link:
                        st.markdown(f"""
                        <div style="background: #0f1f16; border: 1px solid #2a4a35;
                        padding: 14px 18px; margin-bottom: 24px; font-family: DM Mono,
                        monospace; font-size: 11px; color: #4a9463;">
                        TEAM CHAT &nbsp;·&nbsp;
                        <a href="{existing_link}" target="_blank"
                        style="color: #4a9463; text-decoration: none;">
                        Join WhatsApp Group
                        </a>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        with st.form(f"wa_form_{brief_url}"):
                            wa_link = st.text_input("Paste WhatsApp group invite link")
                            if st.form_submit_button("Save Group Link", type="primary"):
                                if wa_link.strip():
                                    save_whatsapp_link(brief_url, wa_link.strip())
                                    st.success("WhatsApp link saved.")
                                    st.rerun()

                    st.divider()

                    # Status updates
                    st.markdown("""
                    <div style="font-family: DM Mono, monospace; font-size: 10px;
                    color: #4a4a4a; letter-spacing: 1.5px; margin-bottom: 16px;">UPDATE STATUS</div>
                    """, unsafe_allow_html=True)

                    if status in ["assigned", "discussing"]:
                        with st.form(f"pitch_form_{brief_url}"):
                            pitch_proof = st.text_input("Paste proof of pitch — screenshot link, email thread, etc.")
                            if st.form_submit_button("Mark as Pitched", type="primary"):
                                if pitch_proof:
                                    update_team_status(brief_url, "pitched", {"pitch_proof": pitch_proof})
                                    st.success("Status updated to pitched.")
                                    st.rerun()

                    if status == "pitched":
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Mark as Hired", key=f"hired_{brief_url}", type="primary"):
                                update_team_status(brief_url, "hired")
                                st.success("Congratulations. Status updated to hired.")
                                st.rerun()
                        with col2:
                            with st.form(f"reject_form_{brief_url}"):
                                reason = st.text_input("Reason for rejection")
                                if st.form_submit_button("Mark as Rejected"):
                                    update_team_status(brief_url, "rejected", {"rejection_reason": reason})
                                    st.info("A new brief will be assigned soon.")
                                    st.rerun()

                    if status == "hired":
                        with st.form(f"submit_form_{brief_url}"):
                            deliverable = st.text_input("Deliverable link or description")
                            if st.form_submit_button("Submit Final Work", type="primary"):
                                if deliverable:
                                    update_team_status(brief_url, "submitted", {"deliverable": deliverable})
                                    st.success("Work submitted. Verified record will be generated.")
                                    st.rerun()

                    if status == "submitted":
                        st.markdown("""
                        <div style="background: #0f1f16; border: 1px solid #2a4a35;
                        padding: 20px; font-family: DM Sans, sans-serif; font-size: 13px; color: #4a9463;">
                        Work submitted. Your verified record is being generated.
                        </div>
                        """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

    # ─────────────────────────────────────────
    # TEAM CHAT
    # ─────────────────────────────────────────
    elif page == "Team Chat":

        st.markdown('<div class="page-title">Team Chat.</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Discuss your brief with your team</div>', unsafe_allow_html=True)

        try:
            from database.teams import get_teams_by_member
            from database.messages import send_message, get_messages
            from database.opportunities import get_open_briefs
            from database.auth import get_user_by_email

            user_email = user["email"]
            user_name = user["name"]
            my_teams = get_teams_by_member(user_email)

            if not my_teams:
                st.markdown("""
                <div style="border: 1px solid #1e1e1e; padding: 40px; text-align: center;
                font-family: DM Mono, monospace; font-size: 12px; color: #4a4a4a;">
                You are not assigned to a team yet.
                </div>
                """, unsafe_allow_html=True)
            else:
                briefs = get_open_briefs()

                # If multiple teams pick one
                if len(my_teams) > 1:
                    brief_options = [t["brief_source_url"][:50] for t in my_teams]
                    selected_idx = st.selectbox("Select team", range(len(brief_options)), format_func=lambda i: brief_options[i])
                    active_team = my_teams[selected_idx]
                else:
                    active_team = my_teams[0]

                brief_url = active_team["brief_source_url"]
                brief = next((b for b in briefs if b.get("source_url") == brief_url), None)

                # Show brief context
                if brief:
                    st.markdown(f"""
                    <div style="background: #0f0f0f; border: 1px solid #1e1e1e;
                    border-left: 2px solid #e8e4dc; padding: 16px 20px; margin-bottom: 24px;">
                        <div style="font-family: DM Mono, monospace; font-size: 10px;
                        color: #4a4a4a; margin-bottom: 6px;">BRIEF</div>
                        <div style="font-family: Syne, sans-serif; font-size: 15px;
                        font-weight: 700; color: #e8e4dc;">{brief.get("problem", "N/A")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Show team members
                members = active_team.get("members", [])
                members_html = " &nbsp;·&nbsp; ".join(members)
                st.markdown(f"""
                <div style="font-family: DM Mono, monospace; font-size: 10px;
                color: #4a4a4a; letter-spacing: 1px; margin-bottom: 20px;">
                TEAM: {members_html}
                </div>
                """, unsafe_allow_html=True)

                # Messages
                messages = get_messages(brief_url)

                if messages:
                    for msg in messages:
                        is_mine = msg["sender_email"] == user_email
                        mine_class = "chat-mine" if is_mine else ""
                        ts = msg["timestamp"].strftime("%b %d, %H:%M") if hasattr(msg.get("timestamp"), "strftime") else ""
                        st.markdown(f"""
                        <div class="chat-msg {mine_class}">
                            <div class="chat-sender">{msg["sender_name"]} &nbsp;·&nbsp; {ts}</div>
                            <div class="chat-text">{msg["text"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="font-family: DM Mono, monospace; font-size: 11px;
                    color: #3a3a3a; padding: 20px 0;">
                    No messages yet. Start the conversation.
                    </div>
                    """, unsafe_allow_html=True)

                # Send message
                with st.form("chat_form", clear_on_submit=True):
                    msg_text = st.text_input("Message", placeholder="Type your message...")
                    send = st.form_submit_button("Send", type="primary")
                    if send and msg_text.strip():
                        send_message(brief_url, user_email, user_name, msg_text.strip())
                        st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

    