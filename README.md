# Multi-Agent Creative Studio

A multi-agent AI system that generates, critiques, refines, and presents creative ideas through iterative agent collaboration.

Built with **LangGraph, LangChain, and Google Gemini**, with both a CLI and Streamlit Web UI.

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

## Why Agentic?

* Agent-to-Agent communication through shared LangGraph state
* Autonomous routing based on critic decisions
* Iterative refinement instead of one-shot generation
* Specialized responsibilities for each agent
* Bounded retry loop for controlled execution

## Tech Stack

* **Python 3.10+**
* **Google Gemini Flash**
* **LangGraph**
* **LangChain**
* **Streamlit**

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
