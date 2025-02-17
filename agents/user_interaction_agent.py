from langchain.chat_models import ChatOpenAI
from config import Config

class UserInteractionAgent:
    """
    LLM Agent 3: User Interaction and Validation Agent
    Goal: Understand and validate user requests, then provide clear feedback.
    Model: GPT-4o (assigned via Config).
    """
    def __init__(self):
        self.model = ChatOpenAI(model_name=Config.USER_INTERACTION_MODEL, temperature=0.5)
        self.goal = "Understand and validate user requests, and provide clear confirmations or instructions."

    def handle_interaction(self, payload):
        message = payload.get("message", "No message provided")
        prompt = (
            f"Goal: {self.goal}\n"
            f"Process the following user message and generate an appropriate response:\n{message}\n"
            "Return a clear confirmation or instruction."
        )
        response = self.model.predict(prompt)
        return f"User Interaction response: {response}"
