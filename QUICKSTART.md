# Quick Start Guide

## Multi-Agent Creative Studio - Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Google API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Setup (5 minutes)

#### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/mayankgautam-dev/multi-agent-creative-studio.git
cd multi-agent-creative-studio

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

#### Step 3: Run Validation Tests (Optional)

```bash
# Verify the system structure
python test_structure.py
```

Expected output:
```
✅ All validation tests passed!
```

### Usage

#### Basic Usage - Default Topic

```bash
python main.py
```

This will run the creative studio with a default topic about sustainable living.

#### Custom Topic

```bash
python main.py "Your creative topic here"
```

#### Examples

**Example 1: E-commerce Platform**
```bash
python main.py "An AI-powered e-commerce platform for handmade artisan products"
```

**Example 2: Educational App**
```bash
python main.py "A gamified mobile app to teach children financial literacy"
```

**Example 3: Health & Wellness**
```bash
python main.py "A wearable device that helps manage stress and anxiety through biofeedback"
```

### What Happens When You Run It?

1. **🚀 Initialization**: All 4 agents are initialized with Gemini 2.5 Flash
2. **💡 Step 1**: Idea Agent generates 3 creative concepts
3. **🔍 Step 2**: Critic Agent analyzes the ideas (A2A communication)
4. **✨ Step 3**: Refiner Agent improves ideas based on critique (A2A communication)
5. **📊 Step 4**: Presenter Agent creates final presentation (A2A communication)
6. **💾 Output**: Saves a markdown file with complete results

### Output

The system generates a file named `creative_studio_output_YYYYMMDD_HHMMSS.md` containing:

- Executive Summary
- Creative Process Overview
- 3 Final Refined Ideas
- Comparison Analysis
- Next Steps and Action Items

### Example Output Structure

```markdown
# Multi-Agent Creative Studio Output

**Topic:** Your Topic Here
**Generated:** 2024-12-21T10:30:45

---

## EXECUTIVE SUMMARY
[Overview of the project]

## CREATIVE PROCESS OVERVIEW
[How ideas were developed]

## FINAL RECOMMENDATIONS
### Idea 1: [Title]
- Description
- Target Audience
- Implementation Roadmap
- Expected Outcomes

[... Ideas 2 & 3 ...]

## COMPARISON ANALYSIS
[How ideas evolved]

## NEXT STEPS
[Action items and timeline]
```

### Programmatic Usage

You can also use the studio programmatically:

```python
import os
from dotenv import load_dotenv
from main import CreativeStudio

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Create studio instance
studio = CreativeStudio(api_key)

# Run creative workflow
results = studio.run("Your creative topic", save_output=True)

# Access results
print(results['topic'])
print(results['final_output']['presentation'])
```

### Troubleshooting

#### "GOOGLE_API_KEY not found"
- Make sure you created the `.env` file
- Verify your API key is correctly set in the `.env` file
- Try: `export GOOGLE_API_KEY=your_key` in the terminal

#### Import Errors
- Run: `pip install -r requirements.txt`
- Verify Python 3.8+ is installed: `python --version`

#### API Errors
- Check your API key is valid at [Google AI Studio](https://makersuite.google.com/)
- Ensure you have API quota available
- Verify internet connectivity

### Tips for Best Results

1. **Be Specific**: Provide clear, detailed topics
   - ❌ "A new app"
   - ✅ "A mobile app for remote teams to play interactive games during virtual meetings"

2. **Use Context**: Include target audience or constraints
   - ✅ "A fitness app for seniors with mobility challenges"

3. **Specify Domain**: Mention the industry or field
   - ✅ "An IoT solution for smart agriculture in developing countries"

### Performance

- **Duration**: Typically 1-3 minutes per complete workflow
- **API Calls**: 4 calls to Gemini 2.5 Flash (one per agent)
- **Output Size**: Usually 2-5 KB markdown file

### Next Steps

1. **Explore**: Try different topics and see how ideas evolve
2. **Customize**: Modify agent prompts in `*_agent.py` files
3. **Extend**: Add new agents to the pipeline
4. **Integrate**: Use the CreativeStudio class in your own projects

### Learn More

- 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- 📘 Check [README.md](README.md) for comprehensive documentation
- 🧪 Run `test_structure.py` to understand the system

### Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review example outputs

---

**Happy Creating! 🎨✨**
