from typing import List, Dict

from agno.agent import Agent
from agno.models.ollama import Ollama

from config import config

from src.prompt_templates import (
    SYSTEM_PROMPT,
    LEGAL_REASONING_PROMPT,
    TOOL_USAGE_PROMPT,
    REFUSAL_PROMPT,
    FINAL_RESPONSE_PROMPT,
)

from src.agent.tools import legal_web_search
from src.agent.planner_agent import PlannerAgent


class ChaanakyaAgent:
    """
    Core agent wrapper for The Chaanakya.

    - Ollama-backed local LLM
    - Explicit conversational memory (history injected into prompt)
    - Planner-controlled live legal web search
    """

    # 🔒 How many past turns to keep (prevents slowdowns)
    MAX_HISTORY_TURNS = 6   # (user + assistant pairs)

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.planner = PlannerAgent()
        self.history: List[Dict[str, str]] = []

        # Initialize agent with search enabled by default
        self.agent = self._create_agent(enable_search=True)

    # -------------------------
    # Agent Initialization
    # -------------------------

    def _create_agent(self, enable_search: bool) -> Agent:
        tools = [legal_web_search] if enable_search else []

        return Agent(
            name=f"{config.APP_NAME}-{self.session_id}",
            model=Ollama(id=config.OLLAMA_MODEL_NAME),
            instructions=[
                SYSTEM_PROMPT,
                LEGAL_REASONING_PROMPT,
                TOOL_USAGE_PROMPT,
                REFUSAL_PROMPT,
                FINAL_RESPONSE_PROMPT,
            ],
            tools=tools,
            markdown=True,
        )

    # -------------------------
    # Memory Handling
    # -------------------------

    def _build_conversation_context(self) -> str:
        """
        Builds a compact conversation context for the LLM
        using the most recent turns only.
        """

        # Keep only last N turns (each turn = user + assistant)
        recent_history = self.history[-(self.MAX_HISTORY_TURNS * 2):]

        context_lines = []
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_lines.append(f"{role}: {msg['content']}")

        return "\n".join(context_lines)

    # -------------------------
    # Helper function
    # -------------------------

    def _is_farewell(self, user_input: str) -> bool:
        text = user_input.strip().lower()
        return text in {
            "bye",
            "bye!",
            "goodbye",
            "thanks",
            "thanks!",
            "thank you",
            "thank you!",
            "ok thanks",
            "ok thanks bye",
            "ok thanks, bye",
        }

    # -------------------------
    # Public Interface
    # -------------------------

    def run(self, user_input: str) -> str:
        """
        Executes the agent with planner-controlled tools
        and memory-aware prompting.
        """

        # ✅ HARD STOP for farewell
        if self._is_farewell(user_input):
            farewell_response = (
                "You're welcome 🙂 If you need legal help again, feel free to ask. Take care!"
            )
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": farewell_response})
            return farewell_response

        # 1️⃣ Store user message
        self.history.append({"role": "user", "content": user_input})

        # 2️⃣ Planner decides whether search is needed
        decision = self.planner.decide(user_input)
        self.agent = self._create_agent(enable_search=(decision == "SEARCH"))

        # 3️⃣ Build memory-aware prompt
        conversation_context = self._build_conversation_context()

        prompt = (
            "Below is the conversation so far:\n\n"
            f"{conversation_context}\n\n"
            "Now respond to the latest user message appropriately."
        )

        # 4️⃣ Run agent
        response = self.agent.run(prompt).content

        # 5️⃣ Store assistant response
        self.history.append({"role": "assistant", "content": response})

        return response

    def get_conversation(self) -> List[Dict[str, str]]:
        """
        Returns conversation history for UI rendering.
        """
        return self.history

    def reset(self) -> None:
        """
        Resets the conversation.
        """
        self.history = []
        self.agent = self._create_agent(enable_search=True)
