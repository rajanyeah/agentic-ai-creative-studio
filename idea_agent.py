"""
Idea Agent - Generates 3 creative concepts
"""
from google import genai
from google.genai import types


class IdeaAgent:
    """Agent responsible for generating creative concepts"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """Initialize the Idea Agent with Gemini model"""
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.name = "Idea Agent"
    
    def generate_ideas(self, topic: str) -> dict:
        """
        Generate 3 creative concepts based on the given topic
        
        Args:
            topic: The topic or theme for idea generation
            
        Returns:
            dict: Contains the topic and 3 generated ideas
        """
        prompt = f"""You are a creative Idea Agent. Generate 3 unique and innovative creative concepts for the following topic:

Topic: {topic}

For each idea, provide:
1. A catchy title
2. A brief description (2-3 sentences)
3. Key unique selling points

Format your response as:

IDEA 1:
Title: [Title]
Description: [Description]
USP: [Key points]

IDEA 2:
Title: [Title]
Description: [Description]
USP: [Key points]

IDEA 3:
Title: [Title]
Description: [Description]
USP: [Key points]

Be creative, innovative, and think outside the box!"""
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        ideas_text = response.text
        
        return {
            "agent": self.name,
            "topic": topic,
            "ideas": ideas_text,
            "status": "generated"
        }
    
    def __str__(self):
        return f"{self.name} (Gemini-powered creative concept generator)"
