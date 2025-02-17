from langchain.chat_models import ChatOpenAI
from config import Config

class DeveloperAgent:
    """
    LLM Agent 5: Developer/Operator Agent
    Goal: Identify technical issues and suggest corrective actions.
    Model: GPT-4-dev (assigned via Config).
    """
    def __init__(self):
        self.model = ChatOpenAI(model_name=Config.DEVELOPER_AGENT_MODEL, temperature=0.4)
        self.goal = "Identify technical issues and suggest corrective actions."

    def perform_dev_ops(self, payload):
        command = payload.get("command", "check_system")
        prompt = (
            f"Goal: {self.goal}\n"
            f"Execute the following command: {command}\n"
            "Provide a detailed technical response."
        )
        response = self.model.predict(prompt)
        return f"Developer Ops response: {response}"
