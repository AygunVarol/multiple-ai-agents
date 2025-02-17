# app.py
import os
from flask import Flask, request, jsonify, render_template
import threading

from config import Config
from supervisor.supervisor_agent import SupervisorAgent
from services.background_worker import TaskQueue
from services.log_manager import log_manager
from services.metrics_manager import metrics_manager

# Robust Monitoring: Initialize Sentry if SENTRY_DSN is set
if os.environ.get("SENTRY_DSN"):
    import sentry_sdk
    sentry_sdk.init(dsn=os.environ["SENTRY_DSN"])

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the Supervisor Agent
supervisor_agent = SupervisorAgent()

# Start a background task queue if needed
task_queue = TaskQueue()
worker_thread = threading.Thread(target=task_queue.run, daemon=True)
worker_thread.start()

@app.route("/")
def index():
    """Render a simple UI for demonstration."""
    return render_template("index.html")

@app.route("/assign_task", methods=["POST"])
def assign_task():
    """
    Receives JSON payload:
      {
        "task_type": "sensor_management",
        "payload": { ... }
      }
    The Supervisor Agent dispatches the task to the appropriate GPT‑based agent.
    """
    data = request.get_json() or {}
    task_type = data.get("task_type")
    payload = data.get("payload", {})

    if not task_type:
        return jsonify({"error": "Missing 'task_type' in request"}), 400

    try:
        result = supervisor_agent.handle_task(task_type, payload)
        return jsonify({"result": result}), 200
    except Exception as e:
        log_manager.add_log(f"Error in assign_task: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/sensor_data", methods=["POST"])
def sensor_data():
    """
    Receives sensor data from IoT devices (e.g., Raspberry Pis).
    The Sensor Agent processes the incoming data.
    """
    data = request.get_json() or {}
    try:
        result = supervisor_agent.sensor_agent.process_sensor_data(data)
        return jsonify({"result": result}), 200
    except Exception as e:
        log_manager.add_log(f"Error processing sensor data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/logs", methods=["GET"])
def get_logs():
    """Return application logs."""
    logs = log_manager.get_logs()
    return jsonify({"logs": logs})

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
