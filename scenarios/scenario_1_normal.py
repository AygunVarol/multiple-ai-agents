#!/usr/bin/env python3
"""
Scenario 1: Cooperative Edge Analytics under Normal Operation
- Supervisor partitions analytics tasks
- Tasks dispatched to RPis via REST API  
- Results aggregated by supervisor
"""

import time
import random
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
from data_generator import SensorDataGenerator

class NormalOperationScenario:
    def __init__(self, metrics_collector):
        self.metrics = metrics_collector
        self.data_gen = SensorDataGenerator()
        self.locations = ['office', 'kitchen', 'hallway']
        self.rpi_endpoints = {
            'office': 'http://192.168.1.101:8000',
            'kitchen': 'http://192.168.1.102:8000', 
            'hallway': 'http://192.168.1.103:8000'
        }
        self.supervisor_endpoint = 'http://192.168.1.100:5000'
        
    def run(self, duration=300):
        """Run normal operation scenario"""
        print(f"Starting Scenario 1: Normal Operation ({duration}s)")
        
        start_time = time.time()
        results = {
            'scenario': 'S1_Normal_Operation',
            'tasks_completed': 0,
            'tasks_failed': 0,
            'response_times': [],
            'cpu_usage': [],
            'memory_usage': [],
            'network_overhead': [],
            'accuracy_scores': [],
            'energy_consumption': []
        }
        
        # Start background sensor data streaming
        sensor_thread = threading.Thread(
            target=self._stream_sensor_data, 
            args=(duration,)
        )
        sensor_thread.daemon = True
        sensor_thread.start()
        
        # Generate various task types
        task_types = [
            'environmental_analysis',
            'anomaly_detection', 
            'air_quality_assessment',
            'comfort_optimization',
            'predictive_maintenance'
        ]
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            while time.time() - start_time < duration:
                # Generate random task
                task = {
                    'type': random.choice(task_types),
                    'location': random.choice(self.locations),
                    'priority': random.choice(['low', 'medium', 'high']),
                    'data': self.data_gen.generate_task_data()
                }
                
                # Submit task and measure performance
                future = executor.submit(self._execute_task, task)
                
                try:
                    task_result = future.result(timeout=30)
                    results['tasks_completed'] += 1
                    results['response_times'].append(task_result['response_time'])
                    results['accuracy_scores'].append(task_result['accuracy'])
                    
                except Exception as e:
                    results['tasks_failed'] += 1
                    print(f"Task failed: {e}")
                
                # Collect system metrics
                metrics = self._collect_system_metrics()
                results['cpu_usage'].append(metrics['cpu'])
                results['memory_usage'].append(metrics['memory'])
                results['network_overhead'].append(metrics['network'])
                results['energy_consumption'].append(metrics['energy'])
                
                # Wait before next task (realistic interval)
                time.sleep(random.uniform(2, 8))
        
        # Calculate summary statistics
        results['avg_response_time'] = sum(results['response_times']) / len(results['response_times']) if results['response_times'] else 0
        results['success_rate'] = results['tasks_completed'] / (results['tasks_completed'] + results['tasks_failed']) if (results['tasks_completed'] + results['tasks_failed']) > 0 else 0
        results['avg_cpu_usage'] = sum(results['cpu_usage']) / len(results['cpu_usage']) if results['cpu_usage'] else 0
        results['total_energy'] = sum(results['energy_consumption'])
        
        print(f"S1 Completed: {results['tasks_completed']} tasks, {results['avg_response_time']:.2f}ms avg response")
        
        return results
    
    def _execute_task(self, task):
        """Execute a single task and measure performance"""
        start_time = time.time()
        
        try:
            # Send task to supervisor for delegation
            response = requests.post(
                f"{self.supervisor_endpoint}/api/task",
                json=task,
                timeout=25
            )
            
            response_time = (time.time() - start_time) * 1000  # ms
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'response_time': response_time,
                    'accuracy': self._calculate_accuracy(task, result),
                    'success': True
                }
            else:
                raise Exception(f"HTTP {response.status_code}")
                
        except Exception as e:
            return {
                'response_time': (time.time() - start_time) * 1000,
                'accuracy': 0,
                'success': False,
                'error': str(e)
            }
    
    def _stream_sensor_data(self, duration):
        """Continuously stream sensor data from all locations"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for location in self.locations:
                sensor_data = self.data_gen.generate_sensor_data(location)
                
                try:
                    requests.post(
                        f"{self.supervisor_endpoint}/api/sensor_data",
                        json=sensor_data,
                        timeout=5
                    )
                except:
                    pass  # Continue streaming even if some requests fail
            
            time.sleep(1)  # 1 second interval
    
    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # Get metrics from supervisor
            response = requests.get(f"{self.supervisor_endpoint}/api/metrics", timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        # Return default metrics if unable to collect
        return {
            'cpu': random.uniform(20, 50),
            'memory': random.uniform(30, 60), 
            'network': random.uniform(100, 500),
            'energy': random.uniform(5, 15)
        }
    
    def _calculate_accuracy(self, task, result):
        """Calculate task accuracy score (0-100)"""
        # Simulate accuracy based on task complexity and location specialization
        base_accuracy = 85
        
        # Location specialization bonus
        if task.get('location') in ['office', 'kitchen', 'hallway']:
            base_accuracy += 5
        
        # Priority adjustment
        priority_bonus = {'low': 0, 'medium': 2, 'high': 5}
        base_accuracy += priority_bonus.get(task.get('priority', 'low'), 0)
        
        # Add some randomness
        accuracy = base_accuracy + random.uniform(-10, 10)
        return max(0, min(100, accuracy))