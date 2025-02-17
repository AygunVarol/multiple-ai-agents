"""
This module reads sensor data from a BME680 sensor connected to a Raspberry Pi
and sends the data to the local server endpoint (/sensor_data) asynchronously.
It uses aiohttp for non-blocking HTTP requests and implements simple retry logic.
"""

import os
import asyncio
import aiohttp
import time
import logging
import bme680
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

SERVER_URL = Config.SENSOR_SERVER_URL

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

async def send_sensor_data(session, data, retries=3, delay=2):
    """
    Sends sensor data to the server using aiohttp with a simple retry mechanism.
    """
    for attempt in range(1, retries + 1):
        try:
            async with session.post(SERVER_URL, json=data, timeout=5) as response:
                text = await response.text()
                logger.info("Server response: " + text)
                return text
        except Exception as e:
            logger.error(f"Attempt {attempt}: Error sending data to server: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    return "Failed after retries."

async def poll_sensor():
    """
    Asynchronously polls the sensor data and sends it to the server.
    Since sensor.get_sensor_data() is blocking, run it in an executor.
    """
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        while True:
            # Run the blocking sensor read in a thread pool
            sensor_data_ready = await loop.run_in_executor(None, sensor.get_sensor_data)
            if sensor_data_ready:
                data_payload = {
                    "temperature": sensor.data.temperature,
                    "pressure": sensor.data.pressure,
                    "humidity": sensor.data.humidity
                }
                if sensor.data.heat_stable:
                    data_payload["gas"] = sensor.data.gas_resistance

                logger.info(f"Sensor reading: {data_payload}")
                await send_sensor_data(session, data_payload)
            await asyncio.sleep(1)  # Polling interval

if __name__ == '__main__':
    try:
        asyncio.run(poll_sensor())
    except KeyboardInterrupt:
        logger.info("Exiting sensor reading module.")
