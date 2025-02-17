# Multiple AI Agents Framework for Smart Spaces

This project implements a hierarchical multi-agent system designed for smart spaces. It leverages GPT-based models via LangChain to orchestrate various specialized agents that work together to process sensor data, make decisions, interact with users, simulate digital twin scenarios, and assist developers/operations.

The system is designed for indoor environments where multiple IoT devices—such as Raspberry Pis equipped with environmental sensors (e.g., BME680)—continuously send real-time data to a local server. The Supervisor Agent processes natural language commands from users and delegates tasks to the appropriate specialized agents based on their goals and assigned GPT models.

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
        
        git clone https://github.com/aygunvarol/multiple-ai-agents.git
        cd multiple-ai-agents

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
