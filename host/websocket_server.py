import asyncio
import json
import logging
import websockets

from common.logger import setup_logger

logger = setup_logger("websocket_server")

class WebSocketServer:
    def __init__(self, data_queue, host='0.0.0.0', port=8765):
        self.data_queue = data_queue
        self.host = host
        self.port = port
        self.clients = set()

    async def handler(self, websocket, path=None):
        # Register client
        self.clients.add(websocket)
        logger.info(f"Client connected: {websocket.remote_address}")
        try:
            # Keep connection open, listen for incoming messages if needed
            async for _ in websocket:
                pass
        except websockets.ConnectionClosed:
            logger.info(f"Client disconnected: {websocket.remote_address}")
        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message):
        if self.clients:
            disconnected = set()
            for client in self.clients:
                try:
                    await client.send(message)
                except websockets.ConnectionClosed:
                    disconnected.add(client)
            self.clients.difference_update(disconnected)

    async def data_broadcaster(self):
        while True:
            data = await self.data_queue.get()
            try:
                message = json.dumps(data)
                await self.broadcast(message)
                logger.debug(f"Broadcasted: {message}")
            except Exception as e:
                logger.error(f"Failed to broadcast: {e}")

    async def run_server(self):
        logger.info(f"Starting WebSocket server at ws://{self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await self.data_broadcaster()
