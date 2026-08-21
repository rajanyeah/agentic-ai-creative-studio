"""
Idea Agent - Generates 3 creative concepts
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


class IdeaAgent:
    """Agent responsible for generating creative concepts"""

    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """Initialize the Idea Agent with Gemini model"""
        self.llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        self.model_name = model_name
        self.name = "Idea Agent"

    def generate_ideas(self, topic: str, feedback: str = "") -> dict:
        """
        Generate 3 creative concepts based on the given topic

        Args:
            topic: The topic or theme for idea generation
            feedback: Optional critique from a previous round, used to steer regeneration

        Returns:
            dict: Contains the topic and 3 generated ideas
        """
        feedback_block = ""
        if feedback:
            feedback_block = f"""
IMPORTANT: A previous round of these ideas was reviewed and rejected. Address this feedback directly in your new ideas — do not repeat the same weaknesses:

PREVIOUS CRITIQUE:
{feedback}
"""

        prompt = f"""You are a creative Idea Agent. Generate 3 unique and innovative creative concepts for the following topic:

Topic: {topic}
{feedback_block}
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

        response = self.llm.invoke([HumanMessage(content=prompt)])
        ideas_text = self._to_text(response.content)

        return {
            "agent": self.name,
            "topic": topic,
            "ideas": ideas_text,
            "status": "generated"
        }

    def _to_text(self, content) -> str:
        """Normalizes LangChain response content to a plain string.
        Gemini via langchain-google-genai sometimes returns a list of
        content blocks instead of a plain string."""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, str):
                    parts.append(block)
                elif isinstance(block, dict):
                    parts.append(block.get("text", ""))
            return "\n".join(parts)
        return str(content)

    def __str__(self):
        return f"{self.name} (Gemini-powered creative concept generator)"