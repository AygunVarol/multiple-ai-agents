"""
Performance metrics collection for scenario evaluation
"""

import time
import json
import psutil
import threading
from pathlib import Path
from collections import defaultdict, deque
from datetime import datetime

class MetricsCollector:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Metrics storage
        self.metrics_history = defaultdict(deque)
        self.current_metrics = {}
        self.collection_active = False
        self.collection_thread = None
        
        # Performance counters
        self.task_counters = defaultdict(int)
        self.response_times = defaultdict(list)
        self.error_counts = defaultdict(int)
        
    def start_collection(self, interval=5):
        """Start continuous metrics collection"""
        if self.collection_active:
            return
        
        self.collection_active = True
        self.collection_thread = threading.Thread(
            target=self._collect_continuously,
            args=(interval,)
        )
        self.collection_thread.daemon = True
        self.collection_thread.start()
    
    def stop_collection(self):
        """Stop continuous metrics collection"""
        self.collection_active = False
        if self.collection_thread:
            self.collection_thread.join(timeout=10)
    
    def _collect_continuously(self, interval):
        """Continuously collect system metrics"""
        while self.collection_active:
            timestamp = time.time()
            
            # System metrics
            system_metrics = {
                'timestamp': timestamp,
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': self._get_network_io(),
                'process_count': len(psutil.pids())
            }
            
            # Store metrics
            for key, value in system_metrics.items():
                if key != 'timestamp':
                    self.metrics_history[key].append((timestamp, value))
                    
                    # Keep only last 1000 measurements
                    if len(self.metrics_history[key]) > 1000:
                        self.metrics_history[key].popleft()
            
            self.current_metrics = system_metrics
            time.sleep(interval)
    
    def _get_network_io(self):
        """Get network I/O statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
        except:
            return {'bytes_sent': 0, 'bytes_recv': 0, 'packets_sent': 0, 'packets_recv': 0}
    
    def record_task_execution(self, task_type, response_time, success=True, location='supervisor'):
        """Record task execution metrics"""
        timestamp = time.time()
        
        # Update counters
        counter_key = f"{location}_{task_type}"
        self.task_counters[counter_key] += 1
        
        if success:
            self.response_times[counter_key].append(response_time)
        else:
            self.error_counts[counter_key] += 1
        
        # Log detailed execution info
        execution_record = {
            'timestamp': timestamp,
            'task_type': task_type,
            'response_time': response_time,
            'success': success,
            'execution_location': location,
            'system_cpu': self.current_metrics.get('cpu_percent', 0),
            'system_memory': self.current_metrics.get('memory_percent', 0)
        }
        
        # Save to file
        self._append_to_file('task_executions.jsonl', execution_record)
    
    def record_scenario_metrics(self, scenario_id, metrics):
        """Record scenario-specific metrics"""
        timestamp = time.time()
        
        scenario_record = {
            'timestamp': timestamp,
            'scenario_id': scenario_id,
            'metrics': metrics
        }
        
        self._append_to_file(f'{scenario_id}_metrics.jsonl', scenario_record)
    
    def get_performance_summary(self):
        """Get summary of performance metrics"""
        summary = {
            'task_summary': dict(self.task_counters),
            'average_response_times': {},
            'error_rates': {},
            'system_utilization': {}
        }
        
        # Calculate average response times
        for task_type, times in self.response_times.items():
            if times:
                summary['average_response_times'][task_type] = {
                    'mean': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times),
                    'count': len(times)
                }
        
        # Calculate error rates
        for task_type, error_count in self.error_counts.items():
            total_attempts = self.task_counters[task_type] + error_count
            if total_attempts > 0:
                summary['error_rates'][task_type] = error_count / total_attempts
        
        # System utilization summary
        if self.metrics_history['cpu_percent']:
            cpu_values = [v for _, v in self.metrics_history['cpu_percent']]
            summary['system_utilization']['cpu'] = {
                'mean': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values)
            }
        
        if self.metrics_history['memory_percent']:
            mem_values = [v for _, v in self.metrics_history['memory_percent']]
            summary['system_utilization']['memory'] = {
                'mean': sum(mem_values) / len(mem_values),
                'max': max(mem_values),
                'min': min(mem_values)
            }
        
        return summary
    
    def _append_to_file(self, filename, data):
        """Append data to JSONL file"""
        filepath = self.output_dir / filename
        with open(filepath, 'a') as f:
            f.write(json.dumps(data, default=str) + '\n')
    
    def export_metrics(self, filename='metrics_export.json'):
        """Export all collected metrics"""
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'task_counters': dict(self.task_counters),
            'response_times': {k: list(v) for k, v in self.response_times.items()},
            'error_counts': dict(self.error_counts),
            'system_metrics_history': {
                k: list(v) for k, v in self.metrics_history.items()
            },
            'performance_summary': self.get_performance_summary()
        }
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return filepath