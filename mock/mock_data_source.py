# mock/mock_data_source.py

import time
import json
import random

class MockSerial:
    def __init__(self, interval=0.2):
        self.interval = interval  # Simulate 100–200ms interval
        self.counter = 0

    def readline(self):
        self.counter += 1
        data = {
            "time": time.time(),
            "voltage": round(random.uniform(11.0, 12.6), 2),
            "current": round(random.uniform(0.5, 2.0), 2),
            "speed": random.randint(0, 40),
            "status": "ok" if random.random() > 0.05 else "warning"
        }
        time.sleep(self.interval)  # Simulate real-time delay
        return (json.dumps(data) + "\n").encode("utf-8")  # Simulate bytes from serial
