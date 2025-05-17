import asyncio
import json
import serial
import serial_asyncio
import logging
import os

from common.logger import setup_logger

logger = setup_logger("serial")

class SerialReader:
    def __init__(self, port=None, baudrate=115200, mock_file=None):
        self.port = port
        self.baudrate = baudrate
        self.mock_file = mock_file

    async def read_loop(self, queue):
        if self.mock_file:
            logger.info(f"Using mock data from {self.mock_file}")
            await self._read_mock(queue)
        else:
            logger.info(f"Using real serial port: {self.port} at {self.baudrate} baud")
            await self._read_serial(queue)

    async def _read_mock(self, queue):
        process = await asyncio.create_subprocess_exec(
            "python", self.mock_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            try:
                data = json.loads(line.decode().strip())
                logger.debug(f"Mock input: {data}")
                await queue.put(data)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid mock JSON: {line} ({e})")

    async def _read_serial(self, queue):
        try:
            reader, _ = await serial_asyncio.open_serial_connection(
                url=self.port, baudrate=self.baudrate
            )
            while True:
                line = await reader.readline()
                try:
                    data = json.loads(line.decode().strip())
                    logger.debug(f"Serial input: {data}")
                    await queue.put(data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid serial JSON: {line} ({e})")
        except serial.SerialException as e:
            logger.error(f"Could not open serial port: {e}")
