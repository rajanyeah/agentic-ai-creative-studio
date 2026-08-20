"""
Refiner Agent - Improves ideas based on critique
"""
from google import genai
from google.genai import types


class RefinerAgent:
    """Agent responsible for refining and improving ideas based on critique"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """Initialize the Refiner Agent with Gemini model"""
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.name = "Refiner Agent"
    
    def refine_ideas(self, critique_data: dict) -> dict:
        """
        Refine and improve ideas based on the critic's feedback
        
        Args:
            critique_data: Dictionary containing critique from the Critic Agent
            
        Returns:
            dict: Contains the refined and improved ideas
        """
        topic = critique_data.get("topic", "Unknown")
        original_ideas = critique_data.get("original_ideas", "")
        critique = critique_data.get("critique", "")
        
        prompt = f"""You are a Refiner Agent. Your job is to improve the creative ideas based on the critic's feedback.

TOPIC: {topic}

ORIGINAL IDEAS:
{original_ideas}

CRITIC'S FEEDBACK:
{critique}

Based on the critique, refine and improve each idea by:
1. Addressing the identified weaknesses
2. Enhancing the strengths
3. Improving feasibility and practicality
4. Making the ideas more market-ready
5. Mitigating the identified risks

Present 3 REFINED IDEAS with:
- Improved Title
- Enhanced Description
- Addressed Concerns
- Added Value Propositions

Format as:

REFINED IDEA 1:
Title: [Improved Title]
Description: [Enhanced Description]
Improvements Made: [What was changed and why]
New Value: [Additional benefits]

REFINED IDEA 2:
[Same format]

REFINED IDEA 3:
[Same format]

Make sure each refined idea is better than the original!"""
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        refined_text = response.text
        
        return {
            "agent": self.name,
            "topic": topic,
            "original_ideas": original_ideas,
            "critique": critique,
            "refined_ideas": refined_text,
            "status": "refined"
        }
    
    def __str__(self):
        return f"{self.name} (Gemini-powered idea refiner)"
