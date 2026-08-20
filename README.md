> **Autonomous Hacks 26 — Online Agentic Hackathon Submission**
>
> **36-Hour Online Hackathon**
> 20 December, 8:00 AM → 21 December, 12:00 PM
>
> **Problem Statement 6:** Multi-Agent Creative Studio
> Built using Agent-to-Agent (A2A) communication and iterative refinement.
>
> Hackathon Website: https://autonomoushacks.co.in/

# Multi-Agent Creative Studio

A multi-agent system that uses Agent-to-Agent (A2A) communication and iterative refinement to generate, critique, refine, and present creative ideas. Built with Google Gemini 3.6 Flash.

Available with both a CLI and a web UI.

## Features

### Multi-Agent Architecture

This project implements a complete creative workflow using four specialized AI agents:

1. **Idea Agent** — Generates three unique creative concepts based on any topic
2. **Critic Agent** — Analyzes flaws, weaknesses, and opportunities in the ideas
3. **Refiner Agent** — Improves ideas based on the critic's feedback
4. **Presenter Agent** — Produces a final structured, professional presentation

### Why Agentic

- **Agent-to-Agent (A2A) Communication** — Agents pass data to each other, creating a seamless workflow
- **Iterative Refinement** — Ideas are progressively improved through multiple stages
- **Specialized Roles** — Each agent has a specific expertise and responsibility
- **Autonomous Decision Making** — Agents process information and make decisions independently

## Technology Stack

- **Language:** Python 3.10+
- **AI Model:** Google Gemini 3.6 Flash (`gemini-3.6-flash`)
- **Framework:** Google ADK (Agent Development Kit)
- **Interfaces:** CLI and Web UI (Streamlit)
- **Libraries:**
  - `google-genai` — Google's Generative AI SDK
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

```
┌─────────────────┐
│   Idea Agent    │ Generates 3 creative concepts
└────────┬────────┘
         │ A2A Communication
         ▼
┌─────────────────┐
│  Critic Agent   │ Analyzes flaws and opportunities
└────────┬────────┘
         │ A2A Communication
         ▼
┌─────────────────┐
│ Refiner Agent   │ Improves ideas based on feedback
└────────┬────────┘
         │ A2A Communication
         ▼
┌─────────────────┐
│Presenter Agent  │ Creates final professional output
└─────────────────┘
```


### Workflow Steps

1. **Generation Phase**
   Idea Agent receives a topic and generates three unique creative concepts with titles, descriptions, and USPs.

2. **Analysis Phase**
   Critic Agent receives ideas from Idea Agent (A2A) and analyzes strengths, weaknesses, feasibility, market potential, and risks.

3. **Refinement Phase**
   Refiner Agent receives critique from Critic Agent (A2A) and improves ideas by addressing weaknesses and enhancing strengths.

4. **Presentation Phase**
   Presenter Agent receives refined ideas from Refiner Agent (A2A) and creates a comprehensive presentation with executive summary, recommendations, and action items, saving the output to a markdown file.

## Output

The system generates a markdown file with the complete creative process and final recommendations.

- **Filename format:** `creative_studio_output_YYYYMMDD_HHMMSS.md`
- **Contents:**
  - Executive Summary
  - Creative Process Overview
  - Final Recommendations (Top 3 Ideas)
  - Comparison Analysis
  - Next Steps and Action Items

## Project Structure

```
agentic-ai-creative-studio/
│
├── main.py                 # Main orchestration script
├── app.py                  # Streamlit web UI
├── idea_agent.py          # Idea generation agent
├── critic_agent. py        # Critique and analysis agent
├── refiner_agent. py       # Idea refinement agent
├── presenter_agent.py     # Final presentation agent
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── .streamlit/            # Streamlit configuration
│   └── config.toml       # UI theme settings
├── README.md             # This file
├── README_UI.md          # Web UI documentation
├── QUICKSTART. md         # Quick start guide
├── ARCHITECTURE.md       # Technical architecture
├── SAMPLE_OUTPUT.md      # Example outputs
├── test_structure.py     # Structure validation tests
└── test_ui.py            # UI tests
```


## Configuration

### Model Selection

By default, the system uses `gemini-3.6-flash`. To use a different model, modify the `model_name` parameter in `main.py`:

```python
studio = CreativeStudio(api_key, model_name="gemini-3.6-flash")
```

### Customizing Agents

Each agent is modular and can be customized independently:
- Modify prompts in the respective agent files
- Adjust response formats
- Add additional analysis criteria

## Use Cases

- **Product Development** — Generate and refine product ideas
- **Marketing Campaigns** — Create campaign concepts
- **Business Strategy** — Develop business ideas and strategies
- **Content Creation** — Generate content themes and approaches
- **Innovation Workshops** — Facilitate brainstorming sessions
- **Startup Ideas** — Validate and improve startup concepts

## Documentation

- [README_UI.md](README_UI.md) — Complete Web UI guide with features and troubleshooting
- [QUICKSTART.md](QUICKSTART.md) — Get started in five minutes
- [ARCHITECTURE.md](ARCHITECTURE.md) — Technical architecture and A2A communication details
- [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md) — Example outputs and use cases

## Contributing

Contributions are welcome. Please feel free to submit a pull request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Google Gemini 3.6 Flash
- Powered by Google ADK (Agent Development Kit)
- Inspired by modern agentic AI architectures

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Built by Rajanya**