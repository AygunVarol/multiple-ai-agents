# config.py
import os
import yaml

class Config:
    CONFIG_FILE = os.environ.get("CONFIG_FILE", "config.yaml")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            file_config = yaml.safe_load(f)
    else:
        file_config = {}

    SECRET_KEY = file_config.get("SECRET_KEY", os.environ.get("SECRET_KEY", "defaultsecret"))
    DEBUG = file_config.get("DEBUG", True)
    HOST = file_config.get("HOST", "0.0.0.0")
    PORT = file_config.get("PORT", 5000)

    # API Keys and model names for GPT-based models via API
    OPENAI_API_KEY = file_config.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", "your-openai-api-key"))

    # Assigned models for each agent
    SENSOR_AGENT_MODEL = file_config.get("SENSOR_AGENT_MODEL", "gpt-4o-mini")
    REASONING_AGENT_MODEL = file_config.get("REASONING_AGENT_MODEL", "gpt-4-o1")
    USER_INTERACTION_MODEL = file_config.get("USER_INTERACTION_MODEL", "gpt-4o")
    DIGITAL_TWIN_MODEL = file_config.get("DIGITAL_TWIN_MODEL", "gpt-4-dt")
    DEVELOPER_AGENT_MODEL = file_config.get("DEVELOPER_AGENT_MODEL", "gpt-4-dev")

    # Sensor server URL for IoT devices
    SENSOR_SERVER_URL = file_config.get("SENSOR_SERVER_URL", os.environ.get("SENSOR_SERVER_URL", "http://192.168.0.101:5000/sensor_data"))
