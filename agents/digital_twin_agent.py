from langchain.chat_models import ChatOpenAI
from config import Config

class DigitalTwinAgent:
    """
    LLM Agent 4: Digital Twin Agent (Monitoring, Data Analytics, and Prediction)
    Goal: Monitor environmental data trends and predict system adjustments.
    Model: GPT-4-dt (assigned via Config).
    """
    def __init__(self):
        self.model = ChatOpenAI(model_name=Config.DIGITAL_TWIN_MODEL, temperature=0.6)
        self.goal = "Analyze environmental data trends and predict system adjustments."

    def monitor_and_update(self, payload):
        action = payload.get("action", "status_check")
        prompt = (
            f"Goal: {self.goal}\n"
            f"Perform the following action: {action}\n"
            "Provide a concise analysis and recommendation."
        )
        response = self.model.predict(prompt)
        return f"Digital Twin response: {response}"
