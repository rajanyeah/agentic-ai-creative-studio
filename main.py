"""
Agentic AI Creative Studio
Main orchestration script with Agent-to-Agent (A2A) communication,
managed by a LangGraph StateGraph with a conditional retry loop
between the Idea Agent and Critic Agent.
"""
import os
import sys
from typing import TypedDict, Callable, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from idea_agent import IdeaAgent
from critic_agent import CriticAgent
from refiner_agent import RefinerAgent
from presenter_agent import PresenterAgent


class StudioState(TypedDict, total=False):
    topic: str
    ideas_data: dict
    critique_data: dict
    refined_data: dict
    presentation_data: dict
    retry_count: int


class CreativeStudio:
    """Main orchestrator for the Agentic AI Creative Studio"""

    MAX_RETRIES = 2  # caps the idea<->critic loop so it can't run forever

    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self._on_step: Optional[Callable[[str, str], None]] = None

        print("🚀 Initializing Agentic AI Creative Studio...")
        self.idea_agent = IdeaAgent(api_key, model_name)
        self.critic_agent = CriticAgent(api_key, model_name)
        self.refiner_agent = RefinerAgent(api_key, model_name)
        self.presenter_agent = PresenterAgent(api_key, model_name)

        print(f"✅ {self.idea_agent}")
        print(f"✅ {self.critic_agent}")
        print(f"✅ {self.refiner_agent}")
        print(f"✅ {self.presenter_agent}")
        print()

        self._graph = self._build_graph()

    def _notify(self, stage: str, status: str):
        """Reports stage progress to an optional external callback (e.g. Streamlit UI)"""
        if self._on_step:
            self._on_step(stage, status)

    # ------------------------------------------------------------------
    # LangGraph nodes
    # ------------------------------------------------------------------
    def _idea_node(self, state: StudioState) -> dict:
        retry_count = state.get("retry_count", 0)
        feedback = state["critique_data"]["critique"] if retry_count > 0 else ""

        self._notify("idea", "running")
        print(f"💡 {'Retry ' + str(retry_count) + ': ' if retry_count else ''}Generating Creative Ideas...")
        ideas_data = self.idea_agent.generate_ideas(state["topic"], feedback=feedback)
        print(f"   ✓ Status: {ideas_data['status']}")
        print()
        self._notify("idea", "complete")

        return {"ideas_data": ideas_data, "retry_count": retry_count + 1}

    def _critic_node(self, state: StudioState) -> dict:
        self._notify("critique", "running")
        print("🔍 Analyzing Ideas...")
        critique_data = self.critic_agent.analyze_ideas(state["ideas_data"])
        print(f"   ✓ Status: {critique_data['status']} | Score: {critique_data['score']}/10 | Verdict: {critique_data['verdict']}")
        print()
        self._notify("critique", "complete")
        return {"critique_data": critique_data}

    def _refiner_node(self, state: StudioState) -> dict:
        self._notify("refine", "running")
        print("✨ Refining Ideas...")
        refined_data = self.refiner_agent.refine_ideas(state["critique_data"])
        print(f"   ✓ Status: {refined_data['status']}")
        print()
        self._notify("refine", "complete")
        return {"refined_data": refined_data}

    def _presenter_node(self, state: StudioState) -> dict:
        self._notify("present", "running")
        print("📊 Creating Final Presentation...")
        presentation_data = self.presenter_agent.create_presentation(state["refined_data"])
        print(f"   ✓ Status: {presentation_data['status']}")
        print()
        self._notify("present", "complete")
        return {"presentation_data": presentation_data}

    def _route_after_critique(self, state: StudioState) -> str:
        verdict = state["critique_data"].get("verdict", "APPROVE")
        if verdict == "REVISE" and state.get("retry_count", 0) < self.MAX_RETRIES:
            print(f"   ↩ Verdict REVISE — sending back to Idea Agent (retry {state['retry_count']}/{self.MAX_RETRIES})")
            print()
            # Reset the idea/critique boxes to pending in the UI so the loop is visible
            self._notify("idea", "pending")
            self._notify("critique", "pending")
            return "idea"
        return "refiner"

    # ------------------------------------------------------------------
    # Graph construction
    # ------------------------------------------------------------------
    def _build_graph(self):
        graph = StateGraph(StudioState)
        graph.add_node("idea", self._idea_node)
        graph.add_node("critic", self._critic_node)
        graph.add_node("refiner", self._refiner_node)
        graph.add_node("presenter", self._presenter_node)

        graph.set_entry_point("idea")
        graph.add_edge("idea", "critic")
        graph.add_conditional_edges(
            "critic",
            self._route_after_critique,
            {"idea": "idea", "refiner": "refiner"}
        )
        graph.add_edge("refiner", "presenter")
        graph.add_edge("presenter", END)

        return graph.compile()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, topic: str, save_output: bool = True, on_step: Optional[Callable[[str, str], None]] = None) -> dict:
        """
        Execute the complete creative workflow via the LangGraph pipeline.

        Args:
            topic: The topic or theme for creative idea generation
            save_output: Whether to save the final presentation to a file
            on_step: Optional callback(stage: str, status: str) fired as each
                     stage starts/completes/resets — lets a UI (e.g. Streamlit)
                     render live progress, including the idea/critic retry loop.
        """
        self._on_step = on_step

        print("=" * 80)
        print(f"🎨 AGENTIC AI CREATIVE STUDIO")
        print(f"📋 Topic: {topic}")
        print("=" * 80)
        print()

        final_state = self._graph.invoke({"topic": topic, "retry_count": 0})

        if save_output:
            filename = self.presenter_agent.save_presentation(final_state["presentation_data"])
            print(f"💾 Output saved to: {filename}")
            print()

        results = {
            "topic": topic,
            "workflow": {
                "step1_ideas": final_state["ideas_data"],
                "step2_critique": final_state["critique_data"],
                "step3_refined": final_state["refined_data"],
                "step4_presentation": final_state["presentation_data"]
            },
            "final_output": final_state["presentation_data"],
            "retry_count": final_state["retry_count"]
        }

        print("=" * 80)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print(f"   (Idea/Critic loop ran {final_state['retry_count']} time(s))")
        print("=" * 80)
        print()

        self._on_step = None
        return results

    def display_summary(self, results: dict):
        print("\n" + "=" * 80)
        print("📈 WORKFLOW SUMMARY")
        print("=" * 80)
        print(f"Topic: {results['topic']}")
        print(f"Idea/Critic retries: {results['retry_count']}")
        print(f"\nAgent Communication Flow (LangGraph-managed):")
        print(f"  1. {self.idea_agent.name} → Generated ideas")
        print(f"  2. {self.critic_agent.name} → Analyzed ideas (may loop back to step 1)")
        print(f"  3. {self.refiner_agent.name} → Refined ideas")
        print(f"  4. {self.presenter_agent.name} → Created presentation")
        print("\nAll agents communicated successfully via A2A protocol!")
        print("=" * 80)


def main():
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        sys.exit(1)

    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "A mobile app for sustainable living and reducing carbon footprint"
        print(f"ℹ️  No topic provided. Using default topic:")
        print(f"   '{topic}'")
        print(f"   Use: python main.py 'your topic here' to specify a custom topic")
        print()

    try:
        studio = CreativeStudio(api_key, model_name="gemini-3.6-flash")
        results = studio.run(topic, save_output=True)
        studio.display_summary(results)

        print("\n🎉 Thank you for using Agentic AI Creative Studio!")
        print("   Powered by Google Gemini 3.6 Flash with LangGraph-managed A2A Communication\n")

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()