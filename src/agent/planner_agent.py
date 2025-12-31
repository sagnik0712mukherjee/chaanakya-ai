from agno.agent import Agent
from agno.models.ollama import Ollama

from config import config

from src.prompt_templates import (
    PLANNER_INSTRUCTIONS
)


class PlannerAgent:
    """
    Lightweight planning agent that decides
    whether live web search is required.
    """

    def __init__(self):

        self.agent = Agent(
            name="Chaanakya-Planner",
            model=Ollama(id=config.OLLAMA_MODEL_NAME),
            instructions=[PLANNER_INSTRUCTIONS],
        )

    def decide(self, user_query: str) -> str:
        """
        Returns either 'SEARCH' or 'NO_SEARCH'
        """
        response = self.agent.run(user_query)
        decision = response.content.strip().upper()

        return decision if decision in {"SEARCH", "NO_SEARCH"} else "SEARCH"
