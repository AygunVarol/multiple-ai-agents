import csv
import os
import time
import uuid

class MetricsManager:
    def __init__(self, filename="metrics_log.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["record_id", "timestamp", "task_type", "latency_ms", "notes"])

    def log_metrics(self, task_type, latency_ms, notes=""):
        record_id = str(uuid.uuid4())
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(self.filename, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([record_id, timestamp, task_type, latency_ms, notes])

# Global instance
metrics_manager = MetricsManager()
