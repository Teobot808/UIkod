from mock.mock_data_source import MockSerial
import time

mock = MockSerial()

for _ in range(5):
    line = mock.readline()
    print(line.decode("utf-8").strip())
    time.sleep(0.2)  # simulate real reading delay
