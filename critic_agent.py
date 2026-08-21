"""
Critic Agent - Analyzes flaws in generated ideas
"""
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


class CriticAgent:
    """Agent responsible for analyzing and critiquing ideas"""

    def __init__(self, api_key: str, model_name: str = "gemini-3.6-flash"):
        """Initialize the Critic Agent with Gemini model"""
        self.llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        self.model_name = model_name
        self.name = "Critic Agent"

    def analyze_ideas(self, ideas_data: dict) -> dict:
        """
        Analyze the generated ideas and identify flaws, weaknesses, and areas for improvement

        Args:
            ideas_data: Dictionary containing ideas from the Idea Agent

        Returns:
            dict: Contains the critique, a numeric score, and an APPROVE/REVISE verdict
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

Provide detailed, constructive feedback that will help improve these ideas. Be thorough but fair.

After your written analysis, end your response with exactly these two lines, filled in:

SCORE: [a single number from 1-10 rating the overall quality of these ideas]
VERDICT: [APPROVE if the ideas are strong enough to move to refinement, or REVISE if the Idea Agent should regenerate them from scratch]"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        critique_text = self._to_text(response.content)

        return {
            "agent": self.name,
            "topic": topic,
            "original_ideas": ideas,
            "critique": critique_text,
            "score": self._extract_score(critique_text),
            "verdict": self._extract_verdict(critique_text),
            "status": "analyzed"
        }

    def _to_text(self, content) -> str:
        """Normalizes LangChain response content to a plain string.
        Gemini via langchain-google-genai sometimes returns a list of
        content blocks instead of a plain string, which breaks regex parsing."""
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

    def _extract_score(self, text: str) -> int:
        match = re.search(r"SCORE:\s*(\d+)", text, re.IGNORECASE)
        return int(match.group(1)) if match else 7

    def _extract_verdict(self, text: str) -> str:
        # Defaults to APPROVE if parsing fails, so a flaky/malformed
        # model response can never trap the graph in an infinite loop.
        match = re.search(r"VERDICT:\s*(APPROVE|REVISE)", text, re.IGNORECASE)
        return match.group(1).upper() if match else "APPROVE"

    def __str__(self):
        return f"{self.name} (Gemini-powered idea analyzer)"