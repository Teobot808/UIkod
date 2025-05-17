from host.serial_reader import SerialReader
from mock.mock_data_source import MockSerial
from common.logger import setup_logger
import time

print("Starting test...")

logger = setup_logger("test_mock_reader")
mock_serial = MockSerial()
reader = SerialReader(mock_class=MockSerial, logger=logger)

for _ in range(5):
    print("Reading line...")
    data = reader.read_line()
    print("Parsed data:", data)
    time.sleep(0.2)
