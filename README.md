# Multi-Agent LLM Smart Environment

A simplified multi-agent framework for smart indoor environments using LLMs and IoT sensors, as presented in the IEEE IoT Magazine paper.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RPi-Office    │    │   RPi-Kitchen   │    │  RPi-Hallway    │
│ (Location Agent)│    │ (Location Agent)│    │ (Location Agent)│
│   BME680 Sensor │    │   BME680 Sensor │    │   BME680 Sensor │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼──────────────┐
                    │     Laptop/Server          │
                    │   (Supervisor Agent)       │
                    │  LLaMA 3.2 1B + OpenAI    │
                    └────────────────────────────┘
```

## Project Structure

```
smart-environment-llm/
├── README.md
├── requirements.txt
├── config.py
├── laptop/                    # Run on laptop/server
│   ├── supervisor_agent.py    # Main supervisor
│   ├── app.py                # Flask server
│   └── utils.py              # Helper functions
├── raspberry_pi/             # Deploy on each RPi
│   ├── location_agent.py     # Location-specific agent
│   ├── sensor_reader.py      # BME680 sensor interface
│   └── config_rpi.py         # RPi configuration
└── shared/                   # Shared utilities
    ├── communication.py      # REST API communication
    └── models.py            # Data models
```

## Quick Start

### 1. Laptop/Server Setup (Supervisor Agent)

```bash
# Clone and setup
git clone <repository-url>
cd smart-environment-llm

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export GROQ_API_KEY="your-groq-key"  # Optional

# Run supervisor
cd laptop
python app.py
```

### 2. Raspberry Pi Setup (Location Agents)

```bash
# On each RPi, install dependencies
pip install -r requirements.txt

# Set location-specific environment
export LOCATION="office"  # or "kitchen" or "hallway"
export SUPERVISOR_URL="http://192.168.1.100:5000"  # Laptop IP

# Run location agent
cd raspberry_pi
python location_agent.py
```

## Configuration

### `config.py` (Laptop)
```python
import os

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Models
    SUPERVISOR_MODEL = "gpt-4o-mini"
    LOCAL_MODEL = "llama3.2:1b"  # Ollama model
    
    # Server
    HOST = "0.0.0.0"
    PORT = 5000
    
    # Thresholds
    CPU_THRESHOLD = 70  # % for load balancing
    LATENCY_THRESHOLD = 2000  # ms for urgency
```

### `config_rpi.py` (Raspberry Pi)
```python
import os

class RPiConfig:
    LOCATION = os.getenv("LOCATION", "office")
    SUPERVISOR_URL = os.getenv("SUPERVISOR_URL", "http://192.168.1.100:5000")
    
    # Sensor settings
    SENSOR_INTERVAL = 1  # seconds
    
    # Local model (if using Ollama on RPi)
    LOCAL_MODEL = "llama3.2:1b"
    USE_LOCAL_MODEL = True
```

## Key Components

### Supervisor Agent (Laptop)
- **Task Orchestration**: Distributes tasks across location agents
- **Load Balancing**: Monitors CPU usage and offloads to RPis when >70%
- **Failover Management**: Handles RPi failures and leader election
- **Cloud Integration**: Uses OpenAI/Groq for complex reasoning tasks

### Location Agents (Raspberry Pi)
- **Environmental Monitoring**: BME680 sensor data collection
- **Local Inference**: Location-specific LLM processing
- **Data Preprocessing**: Anomaly detection and data cleaning
- **Autonomous Operation**: Can elect leader if supervisor fails

## API Endpoints

### Supervisor (Laptop) - Port 5000

```
POST /api/task               # Assign task to location agent
GET  /api/status             # System status
POST /api/sensor_data        # Receive sensor data from RPis
GET  /api/agents             # List active agents
```

### Location Agent (RPi) - Port 8000

```
POST /api/process            # Process local task
GET  /api/health             # Agent health status
GET  /api/sensor             # Current sensor readings
POST /api/leader_election    # Participate in leader election
```

## Usage Examples

### 1. Environmental Query
```bash
curl -X POST http://192.168.1.100:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "analyze_air_quality",
    "location": "office",
    "urgency": "low"
  }'
```

### 2. Real-time Monitoring
```bash
# Get all sensor readings
curl http://192.168.1.100:5000/api/status

# Get specific location data
curl http://192.168.1.101:8000/api/sensor  # Office RPi
```

## Deployment Scenarios

### S1: Normal Operation
- Supervisor distributes tasks based on location expertise
- Each RPi processes location-specific queries
- Results aggregated and returned to user

### S2: Supervisor Failure
- RPis detect supervisor offline
- Leader election among RPis
- Elected leader takes over coordination

### S3: High Load Balancing
- Supervisor monitors CPU usage
- When >70%, offloads inference to RPis
- Dynamic task redistribution

## Dependencies

### `requirements.txt`
```
flask>=2.3.0
requests>=2.31.0
langchain>=0.1.0
openai>=1.0.0
groq>=0.4.0
bme680>=1.1.0
psutil>=5.9.0
threading>=1.0.0
```

## Hardware Requirements

### Laptop/Server (Supervisor)
- CPU: Intel i5+ or equivalent
- RAM: 8GB minimum
- Network: WiFi/Ethernet
- OS: Linux/Windows/macOS

### Raspberry Pi (Location Agents)
- Model: RPi 4/5 (4GB+ RAM recommended)
- Sensor: Bosch BME680 (via I2C)
- Storage: 32GB+ microSD
- OS: Raspberry Pi OS

## Running the System

1. **Start Supervisor** (on laptop):
   ```bash
   cd laptop && python app.py
   ```

2. **Start Location Agents** (on each RPi):
   ```bash
   cd raspberry_pi && python location_agent.py
   ```

3. **Verify Connection**:
   ```bash
   curl http://192.168.1.100:5000/api/status
   ```

## Features

- ✅ Multi-agent coordination
- ✅ Dynamic load balancing  
- ✅ Autonomous failover
- ✅ Location-aware processing
- ✅ Real-time sensor monitoring
- ✅ REST API communication
- ✅ Edge-cloud collaboration

## Performance Metrics

The system tracks:
- **Response Latency**: Task completion time
- **CPU Utilization**: Load balancing decisions
- **Network Overhead**: Communication efficiency  
- **Accuracy**: Location-specific inference quality
- **Energy Consumption**: RPi power usage

## License

MIT License - See LICENSE file for details.

## Citation

If you use this code in your research, please cite:

```bibtex
@article{varol2025multiagent,
  title={Multiple AI/LLM Agent Deployments in Smart Environments},
  author={Varol, Ayg{\"u}n and Motlagh, Naser Hossein and Leino, Mirka and Virkki, Johanna},
  journal={IEEE Internet of Things Magazine},
  year={2025}
}
```