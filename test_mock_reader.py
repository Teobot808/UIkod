# test_mock_reader.py

import asyncio
from host.serial_reader import SerialReader
from common.logger import setup_logger

logger = setup_logger("test_mock_reader")

async def main():
    queue = asyncio.Queue()

    reader = SerialReader(port=None, mock_file="mock/mock_data_source.py")

    async def consume_queue():
        while True:
            data = await queue.get()
            logger.info(f"Got from queue: {data}")

    await asyncio.gather(
        reader.read_loop(queue),
        consume_queue()
    )

if __name__ == "__main__":
    asyncio.run(main())
