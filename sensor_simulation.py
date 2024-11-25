import requests
import random
import time
from datetime import datetime
import math


class SensorSimulator:
    def __init__(self, sensor_id, base_url, interval=30):
        """
        Initialize sensor simulator

        Args:
            sensor_id (str): Unique sensor identifier (format: HHHH1234)
            base_url (str): Base URL of the Flask API
            interval (int): Time interval between readings in seconds
        """
        self.sensor_id = sensor_id
        self.base_url = base_url.rstrip('/')
        self.interval = interval
        self.last_value = 25.0  # Starting value (e.g., for temperature)

    def generate_realistic_value(self):
        """
        Generate a realistic sensor value with small variations.

        Returns:
            float: A value that follows a somewhat natural pattern.
        """
        # Add random walk with constraints to create realistic data
        change = random.uniform(-0.5, 0.5)
        # Add some periodic variation
        time_factor = math.sin(time.time() / 3600) * 2  # Daily-like cycle

        new_value = self.last_value + change + time_factor

        # Keep values within realistic bounds (e.g., 15-35 for temperature)
        new_value = max(15, min(35, new_value))
        self.last_value = new_value
        return round(new_value, 2)

    def send_reading(self):
        """
        Send a single sensor reading to the API.
        """
        reading = {
            'idsensor': self.sensor_id,
            'valor': self.generate_realistic_value()
        }

        try:
            response = requests.post(f"{self.base_url}/api/sensor_data", json=reading)
            if response.status_code == 201:
                print(f"Successfully sent reading: {reading}")
            else:
                print(f"Failed to send reading. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending reading: {e}")

    def run(self):
        """
        Start the sensor simulation.
        """
        print(f"Starting sensor simulation for sensor {self.sensor_id}")
        while True:
            self.send_reading()
            time.sleep(self.interval)


if __name__ == "__main__":
    # Configuration
    SENSOR_ID = "ATVE2828"  # Replace with your ID
    API_URL = "http://localhost:5000"
    INTERVAL = 30  # seconds

    # Create and run simulator
    simulator = SensorSimulator(SENSOR_ID, API_URL, INTERVAL)
    simulator.run()
