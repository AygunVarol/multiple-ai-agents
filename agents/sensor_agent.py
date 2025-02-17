from langchain.chat_models import ChatOpenAI
from config import Config

class SensorAgent:
    """
    LLM Agent 1: Sensor Manager
    Goal: Receive real-time sensor data from multiple Raspberry Pis, clean and validate
          the data (e.g., remove anomalies) and forward the processed data.
    Model: GPT API model (e.g., gpt-4o-mini) assigned via Config.
    """
    def __init__(self):
        self.model = ChatOpenAI(model_name=Config.SENSOR_AGENT_MODEL, temperature=0.3)
        self.goal = "Clean and validate real-time sensor data from multiple IoT devices."
        # Optionally store the latest data from sensors
        self.latest_data = {}

    def manage_sensors(self, payload):
        """
        Handles sensor-related commands when invoked via the Supervisor Agent.
        For example, a 'read_data' command may simulate polling a sensor.
        """
        command = payload.get("command", "read_data")
        if command == "read_data":
            sensor_info = f"Raspberry Pi {payload.get('raspberry_pi_id', 1)} reports temperature=24.5, humidity=40.2, air_quality=120."
            prompt = (
                f"Goal: {self.goal}\n"
                f"Process the following sensor data and remove any anomalies:\n{sensor_info}\n"
                "Return the cleaned data."
            )
            response = self.model.predict(prompt)
            return f"Processed sensor data: {response}"
        elif command == "calibrate_sensor":
            prompt = f"Goal: Calibrate sensor based on the latest readings. Command: {command}."
            response = self.model.predict(prompt)
            return f"Sensor calibration response: {response}"
        elif command == "detect_anomalies":
            prompt = f"Goal: Detect anomalies in the sensor data provided. Data: {payload.get('data', 'No data provided')}."
            response = self.model.predict(prompt)
            return f"Anomaly detection result: {response}"
        else:
            return f"Unknown sensor command: {command}"

    def process_sensor_data(self, data):
        """
        Receives sensor data sent by IoT devices (e.g., via HTTP POST from Raspberry Pis).
        The data is processed (cleaned and validated) using a GPT API call.
        """
        # Convert received data to a string summary
        sensor_info = f"Received sensor data: {data}"
        prompt = (
            f"Goal: {self.goal}\n"
            f"Process the following sensor data and detect any anomalies:\n{sensor_info}\n"
            "Return the cleaned and validated data."
        )
        response = self.model.predict(prompt)
        # Optionally update the internal state with the latest data
        self.latest_data = data
        return f"Sensor Data Processed: {response}"
