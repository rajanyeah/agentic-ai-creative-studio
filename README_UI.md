# Agentic AI Creative Studio - Web UI Guide 🎨

This document explains how to use the web-based user interface for the Multi-Agent Creative Studio, while keeping the original CLI functionality intact.

## 🚀 Quick Start

### Running the Web UI

Start the Streamlit web application:

```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`

### Running the CLI

The original command-line interface still works exactly as before:

```bash
# With custom topic
python main.py "Your creative topic here"

# With default topic
python main.py
```

## 📋 Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `google-genai>=0.2.0` - Google Generative AI SDK
- `python-dotenv>=1.0.0` - Environment variable management
- `streamlit>=1.28.0` - Web UI framework

### 2. Set Up API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

> 💡 **Get your API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to obtain a free API key.

## 🌟 Web UI Features

### 1. Interactive Interface
- **Clean, modern design** with intuitive layout
- **Responsive** - works on desktop, tablet, and mobile

### 2. Topic Input
- Large text area for entering your creative topic
- Placeholder text with example topics
- Character validation and helpful hints

### 3. Real-Time Progress Tracking
The UI shows live progress as each agent works:
- 💡 **Step 1**: Idea Agent - Generating creative concepts
- 🔍 **Step 2**: Critic Agent - Analyzing ideas
- ✨ **Step 3**: Refiner Agent - Refining based on feedback
- 📊 **Step 4**: Presenter Agent - Creating final presentation

Each step updates with:
- Active indicator (🔄) while running
- Completion checkmark (✅) when done
- Visual progress bars and spinners

### 4. Results Display

#### Organized in Tabs
Results are displayed in 5 easy-to-navigate tabs:

1. **💡 Ideas Tab**
   - Original creative concepts generated
   - Three unique ideas with titles and descriptions

2. **🔍 Critique Tab**
   - Critical analysis of each idea
   - Strengths, weaknesses, and opportunities
   - Feasibility and market potential assessment

3. **✨ Refined Ideas Tab**
   - Improved versions of the original ideas
   - Addresses weaknesses identified by the critic
   - Enhanced features and value propositions

4. **📊 Final Presentation Tab**
   - Professional, executive-ready presentation
   - Executive summary
   - Complete recommendations
   - Implementation roadmap
   - Next steps and action items

5. **📥 Download Tab**
   - Download button for markdown file
   - Includes complete workflow results
   - Timestamped filename
   - Ready for sharing or documentation

### 5. Sidebar Features

#### API Key Status
- Visual indicator showing if API key is loaded
- Masked key display for security
- Instructions if key is missing

#### About Section
- Quick overview of the system
- Feature highlights
- Model information

#### Links
- GitHub repository
- Documentation
- API key registration

### 6. Error Handling
- Missing API key warnings
- Network error handling
- API quota exceeded messages
- User-friendly error messages with troubleshooting tips

### 7. Session Management
- Results persist during your session
- Can generate multiple topics in one session
- State preserved between interactions

## 📸 UI Layout

### Header Section
```
🎨 Agentic AI Creative Studio
AI-Powered Creative Idea Generation with Agent-to-Agent Communication

🤖 How It Works
[Visual flow diagram of 4 agents]
```

### Main Section
```
📝 Enter Your Topic
[Text area for topic input]

🚀 Generate Creative Ideas
[Generate button]

🔄 Processing Your Request
[Real-time progress indicators]

🎉 Results
[Tabbed display of all agent outputs]
```

### Sidebar
```
⚙️ Settings
🔑 API Key Status
ℹ️ About
🤖 Model
🔗 Links
```

## 💡 Usage Tips

### 1. Topic Suggestions
Good topics are:
- Specific but not too narrow
- Clear and well-defined
- Open to creative interpretation

Examples:
- ✅ "A mobile app for learning languages through games"
- ✅ "An eco-friendly food delivery service"
- ✅ "Smart home device for elderly care"
- ❌ "Make something good" (too vague)
- ❌ "Develop the ultimate AI system" (too broad)

### 2. Reviewing Results
- Start with the **Ideas** tab to see original concepts
- Check the **Critique** to understand the analysis
- Review **Refined Ideas** to see improvements
- Read the **Final Presentation** for complete recommendations
- Use the **Download** tab to save results

### 3. Multiple Topics
- You can generate ideas for multiple topics in one session
- Results persist until you refresh the page
- Each generation creates a new timestamped file

### 4. Performance
- First request may take 30-60 seconds (initializing agents)
- Subsequent requests are faster
- Progress indicators keep you informed
- Don't refresh the page while processing

## 🔧 Configuration

### Custom Theme
The `.streamlit/config.toml` file contains theme settings:

```toml
[theme]
primaryColor = "#FF6B6B"       # Accent color
backgroundColor = "#FFFFFF"     # Main background
secondaryBackgroundColor = "#F0F2F6"  # Sidebar/cards
textColor = "#262730"          # Text color
font = "sans serif"            # Font family

[server]
maxUploadSize = 5              # Max upload size in MB
```

Modify these to customize the look and feel.

### Port Configuration
To run on a different port:

```bash
streamlit run app.py --server.port 8502
```

### Headless Mode
To run without opening browser automatically:

```bash
streamlit run app.py --server.headless true
```

## 🆚 Web UI vs CLI

| Feature | Web UI | CLI |
|---------|--------|-----|
| **Interface** | Interactive browser | Command line |
| **Progress** | Real-time visual | Text updates |
| **Results** | Tabbed, expandable | Sequential output |
| **Download** | Button click | Auto-saved file |
| **Multiple Topics** | Session-based | Run multiple times |
| **API Key** | From .env | From .env |
| **Best For** | Interactive exploration | Automation, scripts |

## 🐛 Troubleshooting

### Web UI Won't Start
```bash
# Check if Streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install streamlit>=1.28.0
```

### API Key Not Found
1. Verify `.env` file exists in project root
2. Check file contains `GOOGLE_API_KEY=your_key`
3. Restart the Streamlit app
4. Check sidebar for status indicator

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Slow Performance
- First run initializes all agents (slower)
- Check internet connection
- Verify API quota not exceeded
- Try a shorter topic description

### Download Not Working
- Check browser's download settings
- Verify pop-up blocker isn't blocking
- Try a different browser
- Check file permissions

## 📚 Additional Resources

- **Main README**: [README.md](README.md) - Complete project documentation
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- **Sample Output**: [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md) - Example results

## 🤝 Contributing

If you'd like to enhance the web UI:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both web UI and CLI
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with **Streamlit** for the web interface
- Powered by **Google Gemini 2.5 Flash**
- Uses **Google ADK** for agent orchestration

---

**Made with ❤️ by InnoV8 Team**

For questions or issues, please open an issue on GitHub.
