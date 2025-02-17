import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "defaultsecret")
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000

    # API Keys and model names for GPT-based models via API
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")

    # Assigned models for each agent (update with your desired model identifiers)
    SENSOR_AGENT_MODEL = "gpt-4o-mini"       # For sensor data processing and cleaning
    REASONING_AGENT_MODEL = "gpt-4-o1"         # For reasoning and decision-making
    USER_INTERACTION_MODEL = "gpt-4o"          # For user interaction tasks
    DIGITAL_TWIN_MODEL = "gpt-4-dt"            # For digital twin, monitoring, and prediction
    DEVELOPER_AGENT_MODEL = "gpt-4-dev"        # For developer/ops support
