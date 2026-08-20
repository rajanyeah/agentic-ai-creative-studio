# Architecture Documentation

## Multi-Agent Creative Studio - Technical Architecture

### Overview

This Multi-Agent Creative Studio implements an **Agent-to-Agent (A2A) Communication** architecture with **iterative refinement** using Google's Gemini 2.5 Flash model via the Google ADK (Agent Development Kit).

## System Architecture

### Agent-Based Design

The system consists of four specialized AI agents, each with a distinct role and responsibility:

```
┌─────────────────────────────────────────────────────────────────┐
│                   Multi-Agent Creative Studio                    │
│                                                                   │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌──────┐│
│  │   Idea     │───>│   Critic   │───>│  Refiner   │───>│Presen││
│  │   Agent    │    │   Agent    │    │   Agent    │    │ter A.││
│  └────────────┘    └────────────┘    └────────────┘    └──────┘│
│       ↓                 ↓                  ↓                ↓    │
│    Generate          Analyze           Improve          Present  │
│   3 Concepts         Flaws            Based on         Structured│
│                                       Feedback          Output   │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Specifications

#### 1. Idea Agent (`idea_agent.py`)

**Purpose**: Generate creative concepts

**Input**: 
- Topic/theme string

**Output**:
```python
{
    "agent": "Idea Agent",
    "topic": str,
    "ideas": str,  # 3 formatted ideas
    "status": "generated"
}
```

**Responsibilities**:
- Generate 3 unique creative concepts
- Provide title, description, and USPs for each idea
- Think creatively and innovatively

#### 2. Critic Agent (`critic_agent.py`)

**Purpose**: Analyze and critique ideas

**Input**: 
- Ideas data from Idea Agent

**Output**:
```python
{
    "agent": "Critic Agent",
    "topic": str,
    "original_ideas": str,
    "critique": str,
    "status": "analyzed"
}
```

**Responsibilities**:
- Analyze strengths and weaknesses
- Evaluate feasibility and market potential
- Identify risks and challenges
- Provide constructive feedback

#### 3. Refiner Agent (`refiner_agent.py`)

**Purpose**: Improve ideas based on critique

**Input**: 
- Critique data from Critic Agent (includes original ideas + analysis)

**Output**:
```python
{
    "agent": "Refiner Agent",
    "topic": str,
    "original_ideas": str,
    "critique": str,
    "refined_ideas": str,
    "status": "refined"
}
```

**Responsibilities**:
- Address identified weaknesses
- Enhance strengths
- Improve feasibility
- Add value propositions
- Mitigate risks

#### 4. Presenter Agent (`presenter_agent.py`)

**Purpose**: Create final structured presentation

**Input**: 
- Refined data from Refiner Agent (includes full workflow history)

**Output**:
```python
{
    "agent": "Presenter Agent",
    "topic": str,
    "presentation": str,  # Markdown formatted
    "generated_at": str,  # ISO timestamp
    "status": "completed"
}
```

**Responsibilities**:
- Create executive summary
- Document creative process
- Present final recommendations
- Provide comparison analysis
- Suggest next steps

## Agent-to-Agent (A2A) Communication

### Communication Protocol

The A2A communication follows a **sequential pipeline pattern** where each agent:

1. **Receives** structured data from the previous agent
2. **Processes** the data using its specialized capabilities
3. **Augments** the data with its analysis/output
4. **Passes** the enriched data to the next agent

### Data Flow

```python
# Step 1: Idea Generation
topic = "User's creative topic"
ideas_data = idea_agent.generate_ideas(topic)

# Step 2: A2A Communication - Critic receives ideas
critique_data = critic_agent.analyze_ideas(ideas_data)

# Step 3: A2A Communication - Refiner receives critique
refined_data = refiner_agent.refine_ideas(critique_data)

# Step 4: A2A Communication - Presenter receives refined ideas
presentation_data = presenter_agent.create_presentation(refined_data)
```

### Key A2A Features

1. **Data Continuity**: Each agent receives complete context from previous agents
2. **Accumulative Knowledge**: Data structures grow with each step, maintaining full history
3. **Loose Coupling**: Agents are independent and can be modified without affecting others
4. **Traceable**: Complete audit trail of the creative process
5. **Extensible**: New agents can be added to the pipeline

## Iterative Refinement

The system implements iterative refinement through:

1. **Initial Creation** (Idea Agent): Raw creative concepts
2. **Critical Analysis** (Critic Agent): Identification of flaws and opportunities
3. **Improvement** (Refiner Agent): Enhancement based on feedback
4. **Finalization** (Presenter Agent): Professional output

This creates a **quality improvement loop** where ideas evolve through multiple stages of analysis and refinement.

## Technology Stack

### Core Technologies

- **Python 3.8+**: Primary programming language
- **Google Gemini 2.5 Flash**: AI model for all agents
- **google-genai**: Modern Google Generative AI SDK
- **python-dotenv**: Environment configuration

### Model Configuration

```python
# Each agent initializes with:
from google import genai

client = genai.Client(api_key=api_key)
model_name = "gemini-3.6-flash"

# Generate content with:
response = client.models.generate_content(
    model=model_name,
    contents=prompt
)
```

## Design Patterns

### 1. Pipeline Pattern
Agents are organized in a sequential pipeline where output flows from one to the next.

### 2. Strategy Pattern
Each agent implements a specific strategy (generate, analyze, refine, present).

### 3. Accumulator Pattern
Data structures accumulate information as they pass through the pipeline.

### 4. Template Method Pattern
All agents follow a consistent initialization and execution pattern.

## Orchestration

The `CreativeStudio` class in `main.py` orchestrates the entire workflow:

```python
class CreativeStudio:
    def __init__(self, api_key, model_name="gemini-3.6-flash"):
        # Initialize all 4 agents
        self.idea_agent = IdeaAgent(api_key, model_name)
        self.critic_agent = CriticAgent(api_key, model_name)
        self.refiner_agent = RefinerAgent(api_key, model_name)
        self.presenter_agent = PresenterAgent(api_key, model_name)
    
    def run(self, topic, save_output=True):
        # Execute A2A workflow
        ideas_data = self.idea_agent.generate_ideas(topic)
        critique_data = self.critic_agent.analyze_ideas(ideas_data)
        refined_data = self.refiner_agent.refine_ideas(critique_data)
        presentation_data = self.presenter_agent.create_presentation(refined_data)
        return results
```

## Why This is Agentic

This system exemplifies agentic AI because:

1. **Autonomous Agents**: Each agent operates independently with its own logic
2. **Inter-Agent Communication**: Agents communicate through structured data exchange
3. **Specialized Roles**: Each agent has specific expertise and responsibilities
4. **Collaborative**: Agents work together to achieve a common goal
5. **Adaptive**: Output quality improves through agent collaboration
6. **Goal-Oriented**: The system works toward producing high-quality creative output

## Future Enhancements

Potential improvements to the A2A architecture:

1. **Parallel Processing**: Run certain agents concurrently
2. **Feedback Loops**: Allow Critic to re-evaluate refined ideas
3. **Agent Selection**: Dynamically choose agents based on topic
4. **Multi-Model**: Use different Gemini models for different agents
5. **State Management**: Persist workflow state for resumption
6. **Agent Voting**: Multiple agents vote on best ideas
7. **Human-in-the-Loop**: Allow manual intervention at any stage

## Error Handling

Each agent is isolated, so failures are contained:

```python
try:
    ideas_data = idea_agent.generate_ideas(topic)
except Exception as e:
    # Handle Idea Agent failure
    # Other agents are unaffected
```

## Performance Considerations

- **Sequential Execution**: Agents run one after another (not parallel)
- **API Calls**: 4 Gemini API calls per workflow
- **Token Usage**: Each agent uses tokens based on prompt complexity
- **Latency**: Total time = sum of all agent processing times

## Conclusion

This Multi-Agent Creative Studio demonstrates a practical implementation of A2A communication with iterative refinement, showcasing how specialized AI agents can collaborate to produce superior creative output compared to a single monolithic AI system.
