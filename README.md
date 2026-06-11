# Raah 

### Real Work. Real Proof.

An AI-powered platform that breaks the graduate experience trap by finding real unsolved business problems and matching them to student teams automatically.

---

## The Problem

80% of graduates cite the experience trap as their primary barrier to employment.

No experience to get a job. No job to get experience.

Existing solutions—job boards, internship platforms, and online courses—still require experience that graduates do not yet have. Certificates are easy to obtain and difficult to trust.

**Raah breaks this loop.**

---

## What Raah Does

Instead of connecting graduates to jobs, Raah gives them real work before anyone will hire them.

An AI agent continuously scans public forums for real unsolved business problems. It qualifies each problem through multi-step reasoning and automatically matches the right student team based on skills.

The team works on a real deliverable. The business confirms the work. A verified work record is created—not a certificate, not a fake portfolio project, but proof of real work.

---

## How It Works

```text
Agent finds real problem from Reddit, Indie Hackers, and public forums
↓
Agent qualifies it:
Is it real?
Is it specific?
Is it bounded?
Can outsiders solve it?
↓
Structured task brief generated
↓
Student team matched automatically based on skills
↓
Team works, pitches business, and delivers
↓
Verified work record created permanently
```

---

## Tech Stack

| Component       | Technology                            |
| --------------- | ------------------------------------- |
| Agent Framework | Google ADK 2.0                        |
| Opportunity Discovery | Groq Llama 3.3 70B              |
| Search Layer    | Exa + Tavily                          |
| Reasoning       | Groq Llama 3.3 70B via LiteLLM        |
| Database        | MongoDB Atlas                         |
| UI              | Streamlit                             |
| Authentication  | bcrypt + MongoDB                      |

---

## Agent Pipeline

Raah uses a multi-agent workflow built with Google ADK 2.0.

### OpportunityHunter

Uses Groq Llama 3.3 70B with Exa and Tavily search tools to discover real business problems posted publicly online.

**Output:**

* Title
* Source URL
* Date Posted
* Original Description
* Business Problem Summary
* Opportunity Justification

### Qualifier

Uses Groq Llama 3.3 70B to evaluate each opportunity.

Checks:

1. Is the problem real?
2. Is it specific enough?
3. Can an external team solve it?
4. Is the scope bounded?

**Output:**

* Qualification score
* Pass / Reject decision
* Reasoning summary

### BriefGenerator

Converts qualified opportunities into structured project briefs.

**Output:**

* Problem statement
* Deliverables
* Required skills
* Estimated timeline
* Difficulty level

### TeamMatcher

Matches student teams to opportunities using skills and profile data.

**Output:**

* Team assignment
* Project status tracking

---

## Project Structure

```text
raah/
├── agents/
│   ├── opportunity_hunter.py    # Finds real business problems
│   ├── qualifier.py             # Evaluates opportunities
│   ├── brief_generator.py       # Creates structured briefs
│   ├── team_matcher.py          # Matches teams to projects
│   └── workflow.py              # ADK workflow orchestration
│
├── database/
│   ├── mongo_client.py          # MongoDB connection
│   ├── opportunities.py         # Opportunity storage
│   ├── auth.py                  # Authentication
│   ├── teams.py                 # Team management
│   ├── messages.py              # Team communication
│   └── brief_parser.py          # Agent output parsing
├── tools/
|   └── search_tools.py         # search problems
│
├── ui/
│   └── app.py                   # Streamlit application
│
├── .env.example
├── requirements.txt
└── LICENSE
```

---

## Setup

### Prerequisites

* Python 3.11+
* MongoDB Atlas Account
* Groq API Key
* Tavily API Key
* EXA Api Key

### Installation

```bash
git clone https://github.com/yourusername/raah.git
cd raah

python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
TAVILY_API_KEY=your_tavily_api_key
EXA_API_KEY=your_exa_api_key
```

---

## Running the Project

### Run the Opportunity Discovery Pipeline

```bash
python agents/workflow.py
```

### Run Team Matching

```bash
python agents/team_matcher.py
```

### Launch the Web Application

```bash
streamlit run ui/app.py
```

---

## Features

### For Graduates

* Create a profile with skills and field of study
* Automatically receive relevant project opportunities
* Access complete project briefs
* View original business owner context
* Update project status:

  * Assigned
  * Pitched
  * Accepted
  * Rejected
  * Submitted
* Submit final deliverables
* Join project communication groups

### For the Platform

* Continuous opportunity discovery
* Multi-step AI qualification pipeline
* Automated skill-based matching
* End-to-end project tracking
* Verified work records upon completion

---

## Research

Raah was designed using interviews and feedback from 15 graduates.

### Key Findings

* **80%** identified the experience trap as their primary employment barrier.
* **93%** said they would participate in a team-based real-work platform.
* Most common pain points:

  * Lack of experience
  * Lack of professional network
  * Lack of direction

---

## Why Google ADK?

Google ADK 2.0 enables true multi-agent orchestration with shared workflow context.

The workflow executes sequentially:

```text
OpportunityHunter
      ↓
Qualifier
      ↓
BriefGenerator
      ↓
TeamMatcher
```

Each agent reads the shared state produced by the previous agent, eliminating manual data passing and simplifying orchestration.

### Model Selection Strategy

**Groq Llama 3.3 70B**

* Opportunity discovery
* Qualification reasoning
* Brief generation
* Lower operational cost
* Fast inference

This approach reserves Gemini usage for search-intensive tasks while using Groq for reasoning-heavy operations.

---

### Search Tools

**Exa**

Used for:

* Semantic web search
* Founder content discovery
* Startup and business problem retrieval

**Tavily**

Used for:

* Web search enrichment
* Broader source coverage
* Fallback retrieval when needed

Together, Exa and Tavily provide high-quality retrieval while Groq performs reasoning and decision-making across the Raah pipeline.

## Vision

A degree proves education.

A portfolio proves practice.

**Raah proves real work.**

By connecting graduates with real business problems before they enter the job market, Raah creates verifiable evidence of capability that employers can trust.

---

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

Any use of this code in a network-accessible product requires the complete source code of that product to be made publicly available under the same license.

See the `LICENSE` file for details.
