import time, json, random

def generate_mock_data():
    return json.dumps({
        "timestamp": time.time(),
        "speed": round(random.uniform(0, 40), 1),
        "voltage": round(random.uniform(22, 26), 2),
        "current": round(random.uniform(10, 20), 2),
        "motor_temp": round(random.uniform(30, 70), 1),
        "warnings": ["low_voltage"] if random.random() < 0.1 else []
    })

if __name__ == "__main__":
    while True:
        print(generate_mock_data())
        time.sleep(0.2)