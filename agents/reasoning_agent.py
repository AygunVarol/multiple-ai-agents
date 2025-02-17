from langchain.chat_models import ChatOpenAI
from config import Config

class ReasoningAgent:
    """
    LLM Agent 2: Reasoning and Decision-Making Agent
    Goal: Evaluate sensor inputs and other contextual data to decide on environmental controls.
    Model: GPT-4-o1 (assigned via Config).
    """
    def __init__(self):
        self.model = ChatOpenAI(model_name=Config.REASONING_AGENT_MODEL, temperature=0.7)
        self.goal = "Evaluate sensor inputs and decide on optimal environmental controls."

    def perform_reasoning(self, payload):
        query = payload.get("query", "No query provided")
        prompt = (
            f"Goal: {self.goal}\n"
            f"Based on the following input, determine the best course of action:\n{query}\n"
            "Provide a concise decision."
        )
        response = self.model.predict(prompt)
        return f"Reasoning response: {response}"
