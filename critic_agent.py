"""
Critic Agent - Analyzes flaws in generated ideas
"""
from google import genai
from google.genai import types


class CriticAgent:
    """Agent responsible for analyzing and critiquing ideas"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """Initialize the Critic Agent with Gemini model"""
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.name = "Critic Agent"
    
    def analyze_ideas(self, ideas_data: dict) -> dict:
        """
        Analyze the generated ideas and identify flaws, weaknesses, and areas for improvement
        
        Args:
            ideas_data: Dictionary containing ideas from the Idea Agent
            
        Returns:
            dict: Contains the critique and analysis
        """
        topic = ideas_data.get("topic", "Unknown")
        ideas = ideas_data.get("ideas", "")
        
        prompt = f"""You are a critical Critic Agent. Analyze the following creative ideas for the topic "{topic}" and provide constructive criticism.

IDEAS TO ANALYZE:
{ideas}

For each idea, analyze:
1. Strengths: What works well
2. Weaknesses: What needs improvement
3. Feasibility: How practical is it
4. Market potential: Target audience and viability
5. Risks: Potential challenges or pitfalls

Provide detailed, constructive feedback that will help improve these ideas. Be thorough but fair."""
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        critique_text = response.text
        
        return {
            "agent": self.name,
            "topic": topic,
            "original_ideas": ideas,
            "critique": critique_text,
            "status": "analyzed"
        }
    
    def __str__(self):
        return f"{self.name} (Gemini-powered idea analyzer)"
