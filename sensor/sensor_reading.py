"""
This module reads sensor data from a BME680 sensor connected to a Raspberry Pi
and sends the data to the local server endpoint (/sensor_data). The server URL
can be configured via the SENSOR_SERVER_URL environment variable.
"""

import os
import time
import requests
import logging
import bme680

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

# Get server URL from environment or default value
SERVER_URL = os.environ.get("SENSOR_SERVER_URL", "http://192.168.0.101:5000/sensor_data")

logger.info(f"Sending sensor data to: {SERVER_URL}")
logger.info("Press Ctrl+C to exit!")
logger.info("Initializing sensor...")

# Initialize the sensor (try primary, fallback to secondary)
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

logger.info('Calibration data:')
for name in dir(sensor.calibration_data):
    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):
            logger.info(f'{name}: {value}')

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

logger.info('\nInitial reading:')
for name in dir(sensor.data):
    if not name.startswith('_'):
        value = getattr(sensor.data, name)
        logger.info(f'{name}: {value}')

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

def read_and_send_sensor_data():
    """
    Poll the sensor, format the sensor data, and send it to the server.
    """
    if sensor.get_sensor_data():
        output = '{0:.2f} C, {1:.2f} hPa, {2:.2f} %RH'.format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity
        )
        data_payload = {
            "temperature": sensor.data.temperature,
            "pressure": sensor.data.pressure,
            "humidity": sensor.data.humidity
        }
        if sensor.data.heat_stable:
            gas_res = sensor.data.gas_resistance
            output += f", {gas_res:.2f} Ohms"
            data_payload["gas"] = gas_res

        logger.info(output)
        try:
            response = requests.post(SERVER_URL, json=data_payload, timeout=5)
            logger.info("Server response: " + response.text)
        except Exception as e:
            logger.error("Error sending data to server: " + str(e))

if __name__ == '__main__':
    try:
        while True:
            read_and_send_sensor_data()
            time.sleep(1)  # Adjust polling interval as needed
    except KeyboardInterrupt:
        logger.info("Exiting sensor reading module.")
