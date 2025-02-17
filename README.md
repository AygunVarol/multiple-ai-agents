# Multiple AI Agents Framework for Smart Spaces

This project implements a hierarchical multi-agent system designed for smart spaces. It leverages GPT-based models via LangChain to orchestrate various specialized agents that work together to process sensor data, make decisions, interact with users, simulate digital twin scenarios, and assist developers/operations.

The system is designed for indoor environments where multiple IoT devices—such as Raspberry Pis equipped with environmental sensors (e.g., BME680)—continuously send real-time data to a local server. The Supervisor Agent processes natural language commands from users and delegates tasks to the appropriate specialized agents based on their goals and assigned GPT models.

## Features
