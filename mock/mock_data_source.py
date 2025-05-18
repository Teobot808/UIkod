# mock/mock_data_source.py

import time
import json
import random

class MockSerial:
    def __init__(self, interval=0.2):
        self.interval = interval
        self.start_time = time.time()
        self.laps = 0
        self.counter = 0

    def readline(self):
        self.counter += 1
        elapsed = int(time.time() - self.start_time)

        # Update lap count every 60s
        if elapsed // 60 > self.laps:
            self.laps = elapsed // 60

        data = {
            "time": elapsed,  # now an int
            "voltage": round(random.uniform(11.0, 12.6), 2),
            "current": round(random.uniform(0.5, 2.0), 2),
            "speed": random.randint(0, 40),
            "status": "ok" if random.random() > 0.05 else "warning",
            "pwm": random.randint(0, 100),      # <-- added
            "laps": self.laps                   # <-- added
        }

        time.sleep(self.interval)
        return (json.dumps(data) + "\n").encode("utf-8")
