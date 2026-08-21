"""
Agentic AI Creative Studio - Streamlit Web UI
A web-based interface for the Agentic AI creative studio system
"""
import html
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
from io import StringIO
import contextlib

# Import the CreativeStudio from main.py
from main import CreativeStudio


# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agentic AI Creative Studio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# Design system
# Each agent gets its own color running through the whole app: the flow
# boxes, the tab underlines, the stamps. The four colors together form the
# button gradient, so the "Start production" button visually IS the pipeline.
# ----------------------------------------------------------------------------
STAGE_COLORS = {
    "idea":     {"solid": "#3A5CE0", "tint": "#E9EDFB", "name": "Idea Agent",      "num": "01"},
    "critique": {"solid": "#E4402E", "tint": "#FDEAE8", "name": "Critic Agent",    "num": "02"},
    "refine":   {"solid": "#F2A900", "tint": "#FEF6DC", "name": "Refiner Agent",   "num": "03"},
    "present":  {"solid": "#1FAA6E", "tint": "#E4F7EE", "name": "Presenter Agent", "num": "04"},
}
STAGE_ORDER = ["idea", "critique", "refine", "present"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --ink: #1C1C1E;
    --paper: #FAF9F6;
    --card: #FFFFFF;
    --line: #E4E1D8;
    --muted: #8A8573;
    --idea: #3A5CE0;
    --critique: #E4402E;
    --refine: #F2A900;
    --present: #1FAA6E;
}

/* Base type, scoped so we never touch Streamlit's own icon font */
html, body { font-family: 'Source Serif 4', Georgia, serif; }
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    font-family: 'Source Serif 4', Georgia, serif !important;
}
h1, h2, h3, h4, h5, h6,
.sc-title, .flow-name, .stage-title, label,
div.stButton > button, div.stDownloadButton > button,
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
}
.sc-eyebrow, .sc-meta, .stage-num, .stamp, .key-stamp, .model-tag,
.flow-num, .flow-status, code, .error-msg {
    font-family: 'IBM Plex Mono', monospace !important;
}
/* Icon font fix: Streamlit renders icons (like the sidebar collapse arrow,
   "keyboard_double_arrow_right") using the Material Symbols icon font.
   Previously this was set to `revert`, which doesn't restore that font and
   caused the raw icon name to render as text instead of the glyph. */
[data-testid="stIconMaterial"], span[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
}

.stApp { background: var(--paper); }
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
}

/* ---------- Top spectrum bar ---------- */
.top-bar {
    height: 6px;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--idea), var(--critique), var(--refine), var(--present));
    margin-bottom: 1.8rem;
}

/* ---------- Masthead ---------- */
.sc-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.sc-title {
    font-weight: 700;
    font-size: 2.9rem;
    letter-spacing: -0.02em;
    color: var(--ink) !important;
    margin: 0 0 0.9rem 0;
}
.sc-meta { display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; margin-bottom: 2rem; }
.sc-meta .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.sc-meta .label { font-size: 0.8rem; color: var(--ink); font-weight: 600; margin-right: 0.35rem; }
.sc-meta .arrow { color: var(--line); margin: 0 0.15rem; }
@media (max-width: 640px) { .sc-title { font-size: 2rem; } }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] { background: #F1EFE7; border-right: 1px solid var(--line); }
.side-label {
    font-size: 0.68rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--muted); margin: 1.4rem 0 0.5rem 0;
    border-top: 1px solid var(--line); padding-top: 1.1rem;
}
.side-label.first { border-top: none; padding-top: 0; margin-top: 0; }
.key-stamp {
    display: inline-block; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0.3rem 0.7rem; border-radius: 6px; border: 1.5px solid;
}
.key-ok { color: var(--present); border-color: var(--present); background: #E4F7EE; }
.key-missing { color: var(--critique); border-color: var(--critique); background: #FDEAE8; }
.key-caption { font-size: 0.72rem; color: var(--muted); margin-top: 0.5rem; }
.model-tag {
    display: inline-block; font-size: 0.74rem; color: var(--idea); border: 1px solid var(--idea);
    background: #E9EDFB; padding: 0.35rem 0.65rem; border-radius: 6px;
}
section[data-testid="stSidebar"] a { color: var(--idea) !important; }

/* ---------- Input ---------- */
.stTextArea textarea {
    background: var(--card) !important; border: 1.5px solid var(--line) !important;
    border-radius: 10px !important; font-size: 1rem !important; color: var(--ink) !important; padding: 0.9rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--idea) !important; box-shadow: 0 0 0 3px rgba(58,92,224,0.15) !important; outline: none !important;
}

/* ---------- Button: solid blue, matching the primary accent ---------- */
div.stButton > button {
    background: var(--idea);
    color: #fff; border: none; border-radius: 10px; padding: 0.9rem 1.9rem;
    font-weight: 600; letter-spacing: 0.02em; box-shadow: 0 4px 14px rgba(58,92,224,0.28);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
div.stButton > button:hover { filter: brightness(1.08); transform: translateY(-1px); box-shadow: 0 6px 20px rgba(58,92,224,0.38); }
div.stButton > button:disabled { background: var(--line); color: var(--muted); box-shadow: none; filter: none; transform: none; }
div.stButton > button:focus-visible { outline: 2px solid var(--idea); outline-offset: 2px; }

div.stDownloadButton > button {
    background: var(--present); color: #fff; border: none; border-radius: 8px;
    font-size: 0.85rem; letter-spacing: 0.03em; font-weight: 600; padding: 0.7rem 1.3rem;
}
div.stDownloadButton > button:hover { filter: brightness(1.08); }

/* ---------- Flow boxes ---------- */
.flow-row { display: flex; align-items: stretch; gap: 0; margin: 0.4rem 0 2rem 0; }
.flow-box {
    flex: 1; background: var(--card); border: 2px solid var(--line); border-radius: 14px;
    padding: 1.1rem 0.8rem; text-align: center; transition: all 0.25s ease;
}
.flow-box.active { box-shadow: 0 6px 18px rgba(0,0,0,0.08); transform: translateY(-2px); }
.flow-box.active, .flow-box.done { border-color: var(--stage-color); background: var(--stage-tint); }
.flow-num { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.1em; margin-bottom: 0.3rem; }
.flow-box.active .flow-num, .flow-box.done .flow-num { color: var(--stage-color); font-weight: 600; }
.flow-name { font-weight: 600; font-size: 0.92rem; color: var(--ink); margin-bottom: 0.25rem; }
.flow-status { font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
.flow-box.active .flow-status, .flow-box.done .flow-status { color: var(--stage-color); font-weight: 600; }
.flow-arrow { display: flex; align-items: center; justify-content: center; width: 1.7rem; flex: 0 0 auto; font-size: 1.2rem; color: var(--line); }
@media (max-width: 640px) {
    .flow-row { flex-direction: column; gap: 0.6rem; }
    .flow-arrow { display: none; }
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { font-size: 0.88rem; color: var(--muted); padding: 0.7rem 1rem; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--ink) !important; }
.stTabs [data-baseweb="tab-list"] button:nth-child(1)[aria-selected="true"] { color: var(--idea) !important; }
.stTabs [data-baseweb="tab-list"] button:nth-child(2)[aria-selected="true"] { color: var(--critique) !important; }
.stTabs [data-baseweb="tab-list"] button:nth-child(3)[aria-selected="true"] { color: var(--refine) !important; }
.stTabs [data-baseweb="tab-list"] button:nth-child(4)[aria-selected="true"] { color: var(--present) !important; }
.stTabs [data-baseweb="tab-list"] button:nth-child(5)[aria-selected="true"] { color: var(--ink) !important; }
.tab-chip {
    display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.06em; text-transform: uppercase; padding: 0.25rem 0.6rem; border-radius: 6px;
    margin-bottom: 0.9rem;
}

/* ---------- Error state ---------- */
.error-block { border-left: 4px solid var(--critique); background: #FDEAE8; border-radius: 8px; padding: 1rem 1.3rem; margin: 1.2rem 0 0.7rem 0; }
.error-title { font-family: 'Space Grotesk', sans-serif !important; font-weight: 600; color: var(--critique) !important; margin-bottom: 0.4rem; }
.error-msg { font-size: 0.85rem; color: var(--ink) !important; }

/* ---------- Footer ---------- */
.sc-footer {
    margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--line);
    font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: var(--muted); text-align: center;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def load_api_key():
    """Load API key from environment"""
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")


def initialize_session_state():
    """Initialize session state variables"""
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'workflow_running' not in st.session_state:
        st.session_state.workflow_running = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = ""


@contextlib.contextmanager
def capture_output():
    """Context manager to capture stdout output"""
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield new_out
    finally:
        sys.stdout = old_out


# ----------------------------------------------------------------------------
# Header / sidebar
# ----------------------------------------------------------------------------
def display_header():
    st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sc-eyebrow">Agent-to-agent production system</div>', unsafe_allow_html=True)
    st.markdown('<div class="sc-title">Agentic AI Creative Studio</div>', unsafe_allow_html=True)

    meta_parts = []
    for i, key in enumerate(STAGE_ORDER):
        info = STAGE_COLORS[key]
        meta_parts.append(f'<span class="dot" style="background:{info["solid"]};"></span>'
                           f'<span class="label">{info["name"].replace(" Agent", "")}</span>')
        if i < len(STAGE_ORDER) - 1:
            meta_parts.append('<span class="arrow">&rarr;</span>')
    st.markdown(f'<div class="sc-meta">{"".join(meta_parts)}</div>', unsafe_allow_html=True)


def display_sidebar(api_key):
    with st.sidebar:
        st.markdown('<div class="sc-eyebrow first">Studio</div>', unsafe_allow_html=True)
        st.markdown('<div class="side-label first">Key status</div>', unsafe_allow_html=True)
        if api_key:
            st.markdown('<span class="key-stamp key-ok">Key &mdash; loaded</span>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="key-caption">{html.escape(api_key[:8])}&hellip;{html.escape(api_key[-4:])}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<span class="key-stamp key-missing">Key &mdash; missing</span>', unsafe_allow_html=True)
            st.markdown(
                '<div class="key-caption">Add to <code>.env</code>:<br>GOOGLE_API_KEY=your_key_here</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="side-label">About</div>', unsafe_allow_html=True)
        st.markdown(
            "Four agents generate, critique, refine, and present a set of creative "
            "concepts in sequence, each one handing its work to the next."
        )

        st.markdown('<div class="side-label">Model</div>', unsafe_allow_html=True)
        st.markdown('<span class="model-tag">Gemini 3.6 Flash</span>', unsafe_allow_html=True)

        st.markdown('<div class="side-label">Links</div>', unsafe_allow_html=True)
        st.markdown(
            "[GitHub repository](https://github.com/rajanyeah/agentic-ai-creative-studio.git)  \n"
            "[Documentation](README_UI.md)  \n"
            "[Get an API key](https://makersuite.google.com/app/apikey)"
        )


# ----------------------------------------------------------------------------
# Flow boxes (used live during the run, and again as a static summary after)
# ----------------------------------------------------------------------------
def render_flow(stage_status):
    boxes = []
    for i, key in enumerate(STAGE_ORDER):
        info = STAGE_COLORS[key]
        status = stage_status[key]
        css_class = "active" if status == "running" else ("done" if status == "complete" else "")
        status_text = {"pending": "Waiting", "running": "Working&hellip;", "complete": "Done"}[status]
        boxes.append(
            f'<div class="flow-box {css_class}" style="--stage-color:{info["solid"]}; --stage-tint:{info["tint"]};">'
            f'<div class="flow-num">{info["num"]}</div>'
            f'<div class="flow-name">{info["name"]}</div>'
            f'<div class="flow-status">{status_text}</div>'
            f'</div>'
        )
        if i < len(STAGE_ORDER) - 1:
            arrow_color = info["solid"] if status == "complete" else "var(--line)"
            boxes.append(f'<div class="flow-arrow" style="color:{arrow_color};">&rarr;</div>')
    return f'<div class="flow-row">{"".join(boxes)}</div>'


# ----------------------------------------------------------------------------
# Workflow execution
# ----------------------------------------------------------------------------
def run_creative_workflow(topic, api_key):
    """Run the complete creative workflow via the LangGraph-managed studio pipeline"""
    stage_status = {"idea": "pending", "critique": "pending", "refine": "pending", "present": "pending"}
    flow_slot = st.empty()

    def paint():
        flow_slot.markdown(render_flow(stage_status), unsafe_allow_html=True)

    def on_step(stage, status):
        stage_status[stage] = status
        paint()

    paint()
    try:
        studio = CreativeStudio(api_key, model_name="gemini-3.6-flash")
        results = studio.run(topic, save_output=False, on_step=on_step)
        return results, None

    except Exception as e:
        return None, str(e)


# ----------------------------------------------------------------------------
# Results (tabs restored)
# ----------------------------------------------------------------------------
def display_results(results):
    if not results:
        return

    st.markdown("---")
    st.markdown('<div class="sc-eyebrow">Production record</div>', unsafe_allow_html=True)

    all_complete = {k: "complete" for k in STAGE_ORDER}
    st.markdown(render_flow(all_complete), unsafe_allow_html=True)

    workflow = results.get("workflow", {})

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Ideas", "Critique", "Refined Ideas", "Final Presentation", "Download"
    ])

    def chip(key):
        info = STAGE_COLORS[key]
        st.markdown(
            f'<span class="tab-chip" style="background:{info["tint"]}; color:{info["solid"]};">{info["name"]}</span>',
            unsafe_allow_html=True
        )

    with tab1:
        chip("idea")
        ideas_data = workflow.get("step1_ideas", {})
        if ideas_data:
            st.markdown(ideas_data.get("ideas", "No ideas generated."))

    with tab2:
        chip("critique")
        critique_data = workflow.get("step2_critique", {})
        if critique_data:
            st.markdown(critique_data.get("critique", "No critique available."))

    with tab3:
        chip("refine")
        refined_data = workflow.get("step3_refined", {})
        if refined_data:
            st.markdown(refined_data.get("refined_ideas", "No refined ideas available."))

    with tab4:
        chip("present")
        presentation_data = results.get("final_output", {})
        if presentation_data:
            st.markdown(
                f'<div class="key-caption">Generated {html.escape(str(presentation_data.get("generated_at", "Unknown")))}</div>',
                unsafe_allow_html=True
            )
            st.markdown(presentation_data.get("presentation", "No presentation available."))

    with tab5:
        st.markdown(
            "Download the complete presentation as a markdown file, including every "
            "stage's output from ideas through to the final pitch."
        )
        presentation_data = results.get("final_output", {})
        if presentation_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"creative_studio_output_{timestamp}.md"
            content = f"""# Agentic AI Creative Studio Output

**Topic:** {results.get('topic', 'Unknown')}
**Generated:** {presentation_data.get('generated_at', 'Unknown')}
**Agent:** {presentation_data.get('agent', 'Unknown')}

---

{presentation_data.get('presentation', '')}

---

*Generated by Agentic AI Creative Studio*
*Powered by Google Gemini 3.6 Flash*
"""
            st.download_button(
                label="Download presentation (Markdown)",
                data=content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    inject_css()
    initialize_session_state()

    api_key = load_api_key()

    display_header()
    display_sidebar(api_key)

    st.markdown('<div class="sc-eyebrow">The brief</div>', unsafe_allow_html=True)
    topic = st.text_area(
        "What would you like to create ideas about?",
        placeholder="A mobile app for sustainable living and reducing carbon footprint",
        height=100,
        label_visibility="collapsed",
        help="Enter any topic, concept, or problem you'd like creative ideas for"
    )

    generate_button = st.button("Start production", disabled=not api_key or not topic)

    if not api_key:
        st.markdown(
            '<div class="error-block"><div class="error-title">API key required</div>'
            '<div class="error-msg">Add GOOGLE_API_KEY to your .env file to begin.</div></div>',
            unsafe_allow_html=True
        )
        return

    if generate_button and topic:
        results, error = run_creative_workflow(topic, api_key)

        if error:
            st.markdown(
                f'<div class="error-block"><div class="error-title">Production halted</div>'
                f'<div class="error-msg">{html.escape(error)}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                "- Check your internet connection\n"
                "- Verify your API key is valid\n"
                "- Confirm you have API quota remaining"
            )
        else:
            st.session_state.results = results

    if st.session_state.results:
        display_results(st.session_state.results)

    st.markdown(
        '<div class="sc-footer">Agentic AI Creative Studio &middot; built by rajanya; '
        'Gemini 3.6 Flash &middot; Streamlit</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()