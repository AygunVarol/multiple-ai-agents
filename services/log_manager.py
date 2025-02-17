import threading
import time
from collections import deque
import logging

class LogManager:
    def __init__(self, max_logs=1000):
        self.logs = deque(maxlen=max_logs)
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

    def add_log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"[{timestamp}] {message}"
        with self.lock:
            self.logs.append(log_entry)
        logging.info(message)

    def get_logs(self):
        with self.lock:
            return list(self.logs)

    def clear_logs(self):
        with self.lock:
            self.logs.clear()

# Global instance
log_manager = LogManager()
