# host/serial_reader.py

import serial
from common.config import autodetect_serial_port

class SerialReader:
    def __init__(self, port=None, mock_class=None, logger=None):
        self.logger = logger
        if mock_class is not None:
            self.serial = mock_class()
            if self.logger:
                self.logger.info("Using mock serial port.")
        else:
            if port is None:
                port = autodetect_serial_port()
            baudrate = 115200  # Or move to config.py
            try:
                self.serial = serial.Serial(port, baudrate, timeout=1)
                if self.logger:
                    self.logger.info(f"Opened serial port {port} at {baudrate} baud.")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Failed to open serial port {port}: {e}")
                raise


    def read_line(self):
        try:
            line = self.serial.readline()
            if not line:
                return None
            return line.decode('utf-8').strip()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading line from serial port: {e}")
            return None
