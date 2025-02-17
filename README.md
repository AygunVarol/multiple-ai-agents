# Multiple AI Agents Framework for Smart Spaces (Newer Version)

This repository implements a multi-agent system for smart spaces that integrates GPT-based models (via LangChain) and asynchronous sensor data processing. In this version, the system is designed for indoor environments where multiple IoT devices (e.g., Raspberry Pis with BME680 environmental sensors) send real-time data to a local server. Key enhancements include:

- **Asynchronous I/O & Retry Logic:**  
  The sensor module now uses `asyncio` and `aiohttp` for non-blocking sensor polling and network requests, along with a built-in retry mechanism.

- **Enhanced Configuration Management:**  
  Configuration is loaded from a YAML file (if present) as well as environment variables, making it easier to customize settings.

- **Dynamic Model Swapping (AutoGen Placeholder):**  
  The Supervisor Agent provides a method to dynamically update the GPT model used by each agent—paving the way for advanced orchestration (e.g., via AutoGen).

- **Robust Monitoring:**  
  Integration with Sentry (if a DSN is provided) allows external error monitoring and logging.

- **Asynchronous Sensor Data Handling:**  
  The BME680 sensor readings are polled asynchronously with retry logic for robust network communication.

- **Flexible Configuration:**  
  Settings are managed via a YAML configuration file (and environment variables) for easy customization.

- **Dynamic Model Update:**  
  The Supervisor Agent can update agent models on the fly—ideal for integration with dynamic orchestration frameworks like AutoGen.

- **External Error Monitoring:**  
  Sentry integration allows for real-time error tracking if configured.

## Architecture

![LLM Agent2s](https://github.com/user-attachments/assets/f9d214cd-8109-4504-99cc-ebb8b2f59f7c)

## Features

- Multi-Agent Architecture:

        Supervisor Agent: Delegates tasks to five specialized agents.
        
        Sensor Agent: Reads and cleans sensor data from Raspberry Pis.
        
        Reasoning Agent: Evaluates sensor inputs and decides on environmental controls.
        
        User Interaction Agent: Communicates with users, validates commands, and provides feedback.
        
        Digital Twin Agent: Monitors system performance, analyzes trends, and predicts adjustments.
        
        Developer/Operator Agent: Monitors technical issues and assists with debugging and maintenance.

- Real-Time Sensor Data Ingestion:

IoT devices send data via HTTP POST to a dedicated /sensor_data endpoint. The Sensor Agent processes this data using a GPT model via LangChain.

- API-Based GPT Integration:

All agents utilize GPT models (via LangChain) accessed by API calls. Model assignments are configurable via environment variables.

- Background Task Management:

A simple background worker supports asynchronous operations, such as periodic sensor polling.

- Web Interface:

A minimal web UI (using Flask) allows users to send tasks and simulate sensor data input.

## Project Structure

# Multiple AI Agents System

This repository contains a multi-agent system with specialized AI agents managing sensor data, reasoning, user interaction, and digital twin analytics.

## Project Structure

```plaintext
multiple_ai_agents/
├── app.py                         # Main Flask application
├── config.py                      # Configuration settings and API keys
├── sensor/
│   └── sensor_reading.py          # Code for reading BME680 sensor data and sending to server
├── supervisor/
│   └── supervisor_agent.py        # Supervisor Agent that delegates tasks
├── agents/                        # Specialized GPT-based agents
│   ├── sensor_agent.py            # LLM Agent 1: Sensor Manager
│   ├── reasoning_agent.py         # LLM Agent 2: Reasoning and Decision-Making
│   ├── user_interaction_agent.py  # LLM Agent 3: User Interaction and Validation
│   ├── digital_twin_agent.py      # LLM Agent 4: Digital Twin Agent (Monitoring, Analytics, Prediction)
│   └── developer_agent.py         # LLM Agent 5: Developer/Operator Agent
├── services/                      # Support services
│   ├── background_worker.py       # Background task queue for asynchronous operations
│   ├── log_manager.py             # In-memory logging service
│   └── metrics_manager.py         # Performance metrics logging
└── templates/
    └── index.html                 # Simple web interface for task and sensor data simulation
```

## Installation

1. Clone the repository:
        
        git clone https://github.com/yourusername/multiple_ai_agents.git
        cd multiple_ai_agents

2. Create a virtual environment and activate it:

        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

        pip install -r requirements.txt

4. Set environment variables:

Configure the following environment variables either in your shell or by creating a .env file:

    SECRET_KEY
    OPENAI_API_KEY
    SENSOR_SERVER_URL (e.g., http://192.168.0.101:5000/sensor_data)

## How to use?

1. Run the Flask application:

        python app.py

2. Access the Web Interface:

Open your browser and navigate to http://localhost:5000 to view the simple web UI. You can:
- Send tasks to the system (e.g., sensor management, reasoning, etc.).
- Simulate sensor data input from an IoT device.
