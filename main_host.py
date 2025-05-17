import asyncio
from host.serial_reader import SerialReader
from host.websocket_server import WebSocketServer
from common.logger import setup_logger
from common.config import autodetect_serial_port


logger = setup_logger("host")

USE_MOCK = True  # Set to False when running with real Arduino
SERIAL_PORT = autodetect_serial_port() if not USE_MOCK else None  # e.g., COM3 on Windows or /dev/ttyUSB0 on Linux
MOCK_PATH = "mock/mock_data_source.py"

async def main():
    queue = asyncio.Queue()

    # Choose between mock or real serial reader
    reader = SerialReader(
        port=SERIAL_PORT if not USE_MOCK else None,
        mock_file=MOCK_PATH if USE_MOCK else None
    )

    # WebSocket server
    websocket = WebSocketServer(queue)

    # Run both tasks concurrently
    await asyncio.gather(
        reader.read_loop(queue),
        websocket.run_server()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down.")
