import platform
import serial.tools.list_ports

def autodetect_serial_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        raise RuntimeError("No serial ports found.")

    # Filter for common Arduino patterns
    arduino_ports = [
        p.device for p in ports if (
            "Arduino" in p.description or
            "CH340" in p.description or
            "ttyACM" in p.description or
            "USB Serial" in p.description
        )
    ]

    if arduino_ports:
        return arduino_ports[0]
    
    # Fallback: return first port
    return ports[0].device

# Set baudrate constant
SERIAL_BAUDRATE = 115200

# Try to autodetect and set SERIAL_PORT
try:
    SERIAL_PORT = autodetect_serial_port()
except RuntimeError as e:
    print(f"Warning: {e}")
    SERIAL_PORT = None
