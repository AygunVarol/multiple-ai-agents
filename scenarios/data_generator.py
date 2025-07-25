"""
Synthetic sensor data generator for scenario testing
"""

import random
import time
import math
from datetime import datetime, timedelta

class SensorDataGenerator:
    def __init__(self):
        self.location_profiles = {
            'office': {
                'temp_range': (20, 26),
                'humidity_range': (30, 60), 
                'pressure_range': (1010, 1020),
                'air_quality_range': (50, 200),
                'activity_pattern': 'business_hours'
            },
            'kitchen': {
                'temp_range': (18, 35),  # Higher range due to cooking
                'humidity_range': (40, 80),  # Higher humidity
                'pressure_range': (1008, 1018),
                'air_quality_range': (80, 400),  # More variable
                'activity_pattern': 'meal_times'
            },
            'hallway': {
                'temp_range': (19, 24),
                'humidity_range': (35, 55),
                'pressure_range': (1012, 1022),
                'air_quality_range': (30, 150),
                'activity_pattern': 'transit'
            }
        }
    
    def generate_sensor_data(self, location, timestamp=None):
        """Generate realistic sensor data for a specific location"""
        if timestamp is None:
            timestamp = time.time()
        
        profile = self.location_profiles.get(location, self.location_profiles['office'])
        
        # Base values with location-specific characteristics
        temperature = self._generate_temperature(profile, timestamp)
        humidity = self._generate_humidity(profile, timestamp)
        pressure = self._generate_pressure(profile, timestamp)
        air_quality = self._generate_air_quality(profile, timestamp)
        
        # Add some sensor noise and occasional anomalies
        if random.random() < 0.05:  # 5% chance of anomaly
            temperature, humidity, air_quality = self._inject_anomaly(
                temperature, humidity, air_quality, location
            )
        
        return {
            'location': location,
            'timestamp': timestamp,
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'pressure': round(pressure, 2),
            'air_quality': round(air_quality, 2),
            'battery_level': random.uniform(85, 100),  # Simulate sensor battery
            'signal_strength': random.uniform(-60, -30)  # WiFi signal strength
        }
    
    def _generate_temperature(self, profile, timestamp):
        """Generate temperature with daily patterns"""
        temp_min, temp_max = profile['temp_range']
        base_temp = (temp_min + temp_max) / 2
        
        # Daily temperature cycle
        hour = datetime.fromtimestamp(timestamp).hour
        daily_variation = 2 * math.sin((hour - 6) * math.pi / 12)  # Peak at 2 PM
        
        # Activity-based variations
        activity_variation = self._get_activity_variation(profile['activity_pattern'], timestamp)
        
        # Random noise
        noise = random.uniform(-0.5, 0.5)
        
        temperature = base_temp + daily_variation + activity_variation + noise
        return max(temp_min - 2, min(temp_max + 2, temperature))
    
    def _generate_humidity(self, profile, timestamp):
        """Generate humidity with location-specific patterns"""
        hum_min, hum_max = profile['humidity_range']
        base_humidity = (hum_min + hum_max) / 2
        
        # Inverse correlation with temperature (generally)
        hour = datetime.fromtimestamp(timestamp).hour
        daily_variation = -1.5 * math.sin((hour - 6) * math.pi / 12)
        
        # Activity-based variations (cooking increases humidity)
        activity_variation = self._get_humidity_activity_variation(
            profile['activity_pattern'], timestamp
        )
        
        noise = random.uniform(-2, 2)
        
        humidity = base_humidity + daily_variation + activity_variation + noise
        return max(hum_min - 5, min(hum_max + 5, humidity))
    
    def _generate_pressure(self, profile, timestamp):
        """Generate atmospheric pressure with weather patterns"""
        press_min, press_max = profile['pressure_range']
        base_pressure = (press_min + press_max) / 2
        
        # Slow weather-related changes
        weather_cycle = 3 * math.sin(timestamp / 86400 * math.pi / 3)  # 3-day cycle
        
        # Small random variations
        noise = random.uniform(-1, 1)
        
        pressure = base_pressure + weather_cycle + noise
        return max(press_min - 5, min(press_max + 5, pressure))
    
    def _generate_air_quality(self, profile, timestamp):
        """Generate air quality with activity and ventilation patterns"""
        aq_min, aq_max = profile['air_quality_range']
        base_aq = (aq_min + aq_max) / 2
        
        # Activity-based variations
        activity_variation = self._get_air_quality_activity_variation(
            profile['activity_pattern'], timestamp
        )
        
        # Ventilation cycles (air quality improves periodically)
        if random.random() < 0.1:  # 10% chance of ventilation improvement
            ventilation_effect = random.uniform(-20, -5)
        else:
            ventilation_effect = 0
        
        noise = random.uniform(-10, 10)
        
        air_quality = base_aq + activity_variation + ventilation_effect + noise
        return max(aq_min - 20, min(aq_max + 50, air_quality))
    
    def _get_activity_variation(self, pattern, timestamp):
        """Get temperature variation based on activity pattern"""
        hour = datetime.fromtimestamp(timestamp).hour
        
        if pattern == 'business_hours':
            # Higher activity 9 AM - 5 PM
            if 9 <= hour <= 17:
                return random.uniform(0.5, 2.0)
            else:
                return random.uniform(-0.5, 0.5)
                
        elif pattern == 'meal_times':
            # Activity peaks at meal times
            if hour in [7, 8, 12, 13, 18, 19, 20]:
                return random.uniform(2.0, 5.0)  # Cooking heat
            else:
                return random.uniform(-0.5, 0.5)
                
        elif pattern == 'transit':
            # Variable activity throughout day
            return random.uniform(-0.2, 0.8)
        
        return 0
    
    def _get_humidity_activity_variation(self, pattern, timestamp):
        """Get humidity variation based on activity"""
        hour = datetime.fromtimestamp(timestamp).hour
        
        if pattern == 'meal_times':
            # Cooking and cleaning increase humidity
            if hour in [7, 8, 12, 13, 18, 19, 20]:
                return random.uniform(5, 15)
            else:
                return random.uniform(-2, 2)
        
        return random.uniform(-1, 3)
    
    def _get_air_quality_activity_variation(self, pattern, timestamp):
        """Get air quality variation based on activity"""
        hour = datetime.fromtimestamp(timestamp).hour
        
        if pattern == 'business_hours':
            # More people = worse air quality
            if 9 <= hour <= 17:
                return random.uniform(10, 30)
            else:
                return random.uniform(-5, 5)
                
        elif pattern == 'meal_times':
            # Cooking can worsen air quality
            if hour in [7, 8, 12, 13, 18, 19, 20]:
                return random.uniform(20, 60)
            else:
                return random.uniform(-10, 10)
        
        return random.uniform(-5, 15)
    
    def _inject_anomaly(self, temperature, humidity, air_quality, location):
        """Inject realistic anomalies based on location"""
        anomaly_type = random.choice([
            'sensor_drift', 'environmental_event', 'equipment_malfunction'
        ])
        
        if anomaly_type == 'sensor_drift':
            # Gradual sensor calibration drift
            drift = random.uniform(0.5, 3.0)
            temperature += drift
            humidity += drift * 2
            
        elif anomaly_type == 'environmental_event':
            if location == 'kitchen':
                # Cooking event
                temperature += random.uniform(3, 8)
                humidity += random.uniform(10, 25)
                air_quality += random.uniform(50, 150)
            elif location == 'office':
                # HVAC malfunction
                temperature += random.uniform(-5, 5)
                air_quality += random.uniform(20, 80)
            else:  # hallway
                # Door/window opened
                temperature += random.uniform(-3, 3)
                humidity += random.uniform(-10, 10)
                
        elif anomaly_type == 'equipment_malfunction':
            # Sensor giving incorrect readings
            if random.random() < 0.5:
                temperature = random.uniform(-10, 50)  # Clearly wrong reading
            if random.random() < 0.5:
                air_quality = random.uniform(500, 1000)  # Very high reading
        
        return temperature, humidity, air_quality
    
    def generate_task_data(self):
        """Generate data payload for various task types"""
        return {
            'sensor_readings': [
                self.generate_sensor_data('office'),
                self.generate_sensor_data('kitchen'), 
                self.generate_sensor_data('hallway')
            ],
            'time_window': random.randint(60, 3600),  # 1 min to 1 hour
            'analysis_depth': random.choice(['basic', 'detailed', 'comprehensive']),
            'historical_context': random.randint(1, 24)  # Hours of context
        }
    
    def generate_batch_data(self, location, count=100, time_interval=60):
        """Generate a batch of sensor readings over time"""
        current_time = time.time()
        batch = []
        
        for i in range(count):
            timestamp = current_time - (count - i - 1) * time_interval
            reading = self.generate_sensor_data(location, timestamp)
            batch.append(reading)
        
        return batch