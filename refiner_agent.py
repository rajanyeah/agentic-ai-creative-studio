"""
Refiner Agent - Improves ideas based on critique
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


class RefinerAgent:
    """Agent responsible for refining and improving ideas based on critique"""

    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """Initialize the Refiner Agent with Gemini model"""
        self.llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
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

        response = self.llm.invoke([HumanMessage(content=prompt)])
        refined_text = self._to_text(response.content)

        return {
            "agent": self.name,
            "topic": topic,
            "original_ideas": original_ideas,
            "critique": critique,
            "refined_ideas": refined_text,
            "status": "refined"
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
        return f"{self.name} (Gemini-powered idea refiner)"