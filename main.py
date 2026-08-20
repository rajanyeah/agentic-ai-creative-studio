"""
Multi-Agent Creative Studio
Main orchestration script with Agent-to-Agent (A2A) communication

This script coordinates the workflow between four agents:
1. Idea Agent - Generates creative concepts
2. Critic Agent - Analyzes and critiques ideas
3. Refiner Agent - Improves ideas based on critique
4. Presenter Agent - Creates final structured output
"""
import os
import sys
from dotenv import load_dotenv

from idea_agent import IdeaAgent
from critic_agent import CriticAgent
from refiner_agent import RefinerAgent
from presenter_agent import PresenterAgent


class CreativeStudio:
    """Main orchestrator for the Multi-Agent Creative Studio"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """
        Initialize the Creative Studio with all agents
        
        Args:
            api_key: Google API key for Gemini
            model_name: Gemini model to use (default: gemini-3.6-flash)
        """
        self.api_key = api_key
        self.model_name = model_name
        
        # Initialize all agents
        print("🚀 Initializing Multi-Agent Creative Studio...")
        self.idea_agent = IdeaAgent(api_key, model_name)
        self.critic_agent = CriticAgent(api_key, model_name)
        self.refiner_agent = RefinerAgent(api_key, model_name)
        self.presenter_agent = PresenterAgent(api_key, model_name)
        
        print(f"✅ {self.idea_agent}")
        print(f"✅ {self.critic_agent}")
        print(f"✅ {self.refiner_agent}")
        print(f"✅ {self.presenter_agent}")
        print()
    
    def run(self, topic: str, save_output: bool = True) -> dict:
        """
        Execute the complete creative workflow with A2A communication
        
        Args:
            topic: The topic or theme for creative idea generation
            save_output: Whether to save the final presentation to a file
            
        Returns:
            dict: Complete workflow results including all agent outputs
        """
        print("=" * 80)
        print(f"🎨 MULTI-AGENT CREATIVE STUDIO")
        print(f"📋 Topic: {topic}")
        print("=" * 80)
        print()
        
        # Step 1: Idea Agent generates creative concepts
        print("💡 Step 1: Generating Creative Ideas...")
        print(f"   Agent: {self.idea_agent.name}")
        ideas_data = self.idea_agent.generate_ideas(topic)
        print(f"   ✓ Status: {ideas_data['status']}")
        print(f"   ✓ Generated 3 creative concepts")
        print()
        
        # Step 2: Critic Agent analyzes the ideas (A2A Communication)
        print("🔍 Step 2: Analyzing Ideas...")
        print(f"   Agent: {self.critic_agent.name}")
        print(f"   ← Receiving ideas from {self.idea_agent.name}")
        critique_data = self.critic_agent.analyze_ideas(ideas_data)
        print(f"   ✓ Status: {critique_data['status']}")
        print(f"   ✓ Critical analysis completed")
        print()
        
        # Step 3: Refiner Agent improves ideas based on critique (A2A Communication)
        print("✨ Step 3: Refining Ideas...")
        print(f"   Agent: {self.refiner_agent.name}")
        print(f"   ← Receiving critique from {self.critic_agent.name}")
        refined_data = self.refiner_agent.refine_ideas(critique_data)
        print(f"   ✓ Status: {refined_data['status']}")
        print(f"   ✓ Ideas refined and improved")
        print()
        
        # Step 4: Presenter Agent creates final presentation (A2A Communication)
        print("📊 Step 4: Creating Final Presentation...")
        print(f"   Agent: {self.presenter_agent.name}")
        print(f"   ← Receiving refined ideas from {self.refiner_agent.name}")
        presentation_data = self.presenter_agent.create_presentation(refined_data)
        print(f"   ✓ Status: {presentation_data['status']}")
        print(f"   ✓ Professional presentation created")
        print()
        
        # Save the output if requested
        if save_output:
            filename = self.presenter_agent.save_presentation(presentation_data)
            print(f"💾 Output saved to: {filename}")
            print()
        
        # Compile complete workflow results
        results = {
            "topic": topic,
            "workflow": {
                "step1_ideas": ideas_data,
                "step2_critique": critique_data,
                "step3_refined": refined_data,
                "step4_presentation": presentation_data
            },
            "final_output": presentation_data
        }
        
        print("=" * 80)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print()
        
        return results
    
    def display_summary(self, results: dict):
        """Display a summary of the creative process"""
        print("\n" + "=" * 80)
        print("📈 WORKFLOW SUMMARY")
        print("=" * 80)
        print(f"Topic: {results['topic']}")
        print(f"\nAgent Communication Flow:")
        print(f"  1. {self.idea_agent.name} → Generated ideas")
        print(f"  2. {self.critic_agent.name} → Analyzed ideas")
        print(f"  3. {self.refiner_agent.name} → Refined ideas")
        print(f"  4. {self.presenter_agent.name} → Created presentation")
        print("\nAll agents communicated successfully via A2A protocol!")
        print("=" * 80)


def main():
    """Main entry point for the Multi-Agent Creative Studio"""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Get topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "A mobile app for sustainable living and reducing carbon footprint"
        print(f"ℹ️  No topic provided. Using default topic:")
        print(f"   '{topic}'")
        print(f"   Use: python main.py 'your topic here' to specify a custom topic")
        print()
    
    # Initialize and run the studio
    try:
        studio = CreativeStudio(api_key, model_name="gemini-3.6-flash")
        results = studio.run(topic, save_output=True)
        studio.display_summary(results)
        
        print("\n🎉 Thank you for using Multi-Agent Creative Studio!")
        print("   Powered by Google Gemini 2.5 Flash with A2A Communication\n")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
