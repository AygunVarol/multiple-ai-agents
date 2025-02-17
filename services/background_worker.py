import queue
import threading
from services.log_manager import log_manager

class TaskQueue:
    def __init__(self):
        self.tasks = queue.Queue()
        self.running = threading.Event()
        self.running.set()

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))
        log_manager.add_log(f"Task added: {func.__name__} with args={args} kwargs={kwargs}")

    def run(self):
        log_manager.add_log("Task queue started.")
        while self.running.is_set():
            try:
                func, args, kwargs = self.tasks.get(timeout=1)
                log_manager.add_log(f"Executing task: {func.__name__}")
                func(*args, **kwargs)
                self.tasks.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                log_manager.add_log(f"Task error: {str(e)}")
        log_manager.add_log("Task queue stopped.")

    def stop(self):
        self.running.clear()
        log_manager.add_log("Task queue stopping...")
