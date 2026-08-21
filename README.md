# Multi-Agent Creative Studio

A multi-agent system that uses Agent-to-Agent (A2A) communication and iterative refinement to generate, critique, refine, and present creative ideas. Orchestrated with LangGraph and built on Google Gemini 3.6 Flash via LangChain.

Available with both a CLI and a web UI.

## Features

### Multi-Agent Architecture

This project implements a complete creative workflow using four specialized AI agents, coordinated as nodes in a LangGraph state graph:

1. **Idea Agent** — Generates three unique creative concepts based on any topic
2. **Critic Agent** — Analyzes flaws, weaknesses, and opportunities, and returns a structured score and verdict (APPROVE or REVISE)
3. **Refiner Agent** — Improves ideas based on the critic's feedback
4. **Presenter Agent** — Produces a final structured, professional presentation

### Why Agentic

- **Agent-to-Agent (A2A) Communication** — Agents pass structured state to each other through the graph, creating a seamless workflow
- **Conditional Retry Loop** — If the Critic Agent returns a REVISE verdict, the graph routes back to the Idea Agent with the critique folded into the next prompt, rather than moving forward with weak ideas. Capped at two retries to guarantee termination.
- **Iterative Refinement** — Ideas are progressively improved through multiple stages
- **Specialized Roles** — Each agent has a specific expertise and responsibility
- **Autonomous Decision Making** — The Critic Agent's verdict, not a fixed script, determines whether the workflow moves forward or loops back

## Technology Stack

- **Language:** Python 3.10+
- **AI Model:** Google Gemini 3.6 Flash (`gemini-3.6-flash`)
- **Orchestration:** LangGraph — manages agent state, sequencing, and the conditional retry loop between the Idea and Critic agents
- **LLM Integration:** LangChain (`langchain-google-genai`) — wraps Gemini calls for each agent
- **Interfaces:** CLI and Web UI (Streamlit)
- **Libraries:**
  - `langgraph` — Graph-based agent orchestration
  - `langchain-google-genai` — LangChain's Gemini chat model wrapper
  - `python-dotenv` — Environment variable management
  - `streamlit` — Interactive web interface

## Prerequisites

- Python 3.10 or higher
- Google API Key (for Gemini API access)
- pip (Python package manager)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/rajanyeah/agentic-ai-creative-studio.git
cd agentic-ai-creative-studio
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
```

4. **Add your Google API key** to the `.env` file:

## How It Works

Four specialized agents work together through a LangGraph state graph:

```
┌─────────────────┐
│   Idea Agent    │  Generates 3 creative concepts
└────────┬────────┘
         │ A2A Communication
         ▼
┌─────────────────┐
│  Critic Agent   │  Scores ideas, returns APPROVE / REVISE
└────────┬────────┘
         │
         ├── REVISE (retries < max) ──┐
         │                            │
         │      ┌─────────────────────┘
         │      ▼
         │   back to Idea Agent
         │
         └── APPROVE
                │
                ▼
      ┌─────────────────┐
      │ Refiner Agent   │  Improves ideas based on feedback
      └────────┬────────┘
               │ A2A Communication
               ▼
      ┌─────────────────┐
      │Presenter Agent  │  Creates final professional output
      └─────────────────┘
```

If the Critic returns `REVISE`, the workflow loops back to the Idea Agent with the critique included in the next generation. The loop is capped at two retries.

## Agents

| Agent               | Role                                              |
| ------------------- | ------------------------------------------------- |
| **Idea Agent**      | Generates three creative concepts                 |
| **Critic Agent**    | Evaluates ideas and returns `APPROVE` or `REVISE` |
| **Refiner Agent**   | Improves ideas using critic feedback              |
| **Presenter Agent** | Produces the final structured presentation        |

## Setup

```
git clone https://github.com/rajanyeah/agentic-ai-creative-studio.git
cd agentic-ai-creative-studio
pip install -r requirements.txt
cp .env.example .env
```

Add your API key to `.env`:

```
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

### Web UI

```
streamlit run app.py
```

### CLI

```
python main.py "An eco-friendly food delivery service"
```

The system generates a Markdown report containing final recommendations, comparison analysis, and next steps.

## Project Structure

```
agentic-ai-creative-studio/
├── main.py
├── app.py
├── idea_agent.py
├── critic_agent.py
├── refiner_agent.py
├── presenter_agent.py
├── requirements.txt
├── ARCHITECTURE.md
├── README_UI.md
└── SAMPLE_OUTPUT.md
```

## Use Cases

* Product ideation
* Marketing campaigns
* Content creation
* Business strategy
* Startup ideation
* Innovation workshops

## License

MIT

**Built by Rajanya Purohit**
