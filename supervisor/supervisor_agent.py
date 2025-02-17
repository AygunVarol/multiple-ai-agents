from agents.sensor_agent import SensorAgent
from agents.reasoning_agent import ReasoningAgent
from agents.user_interaction_agent import UserInteractionAgent
from agents.digital_twin_agent import DigitalTwinAgent
from agents.developer_agent import DeveloperAgent

from services.log_manager import log_manager

class SupervisorAgent:
    """
    Supervisor Agent:
    - Makes decisions and assigns tasks to specialized agents.
    - Collects and validates sensor data from the Sensor Agent.
    - Coordinates system-wide actions.
    """
    def __init__(self):
        # Instantiate specialized GPT-based agents
        self.sensor_agent = SensorAgent()
        self.reasoning_agent = ReasoningAgent()
        self.user_interaction_agent = UserInteractionAgent()
        self.digital_twin_agent = DigitalTwinAgent()
        self.developer_agent = DeveloperAgent()

    def handle_task(self, task_type, payload):
        log_manager.add_log(f"SupervisorAgent: Handling task '{task_type}'")
        if task_type == "sensor_management":
            return self.sensor_agent.manage_sensors(payload)
        elif task_type == "reasoning":
            return self.reasoning_agent.perform_reasoning(payload)
        elif task_type == "user_interaction":
            return self.user_interaction_agent.handle_interaction(payload)
        elif task_type == "digital_twin":
            return self.digital_twin_agent.monitor_and_update(payload)
        elif task_type == "developer_ops":
            return self.developer_agent.perform_dev_ops(payload)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
