import asyncio
import websockets
import threading
import json
from queue import Queue

class WebsocketServer:
    async def handler(self, websocket, path):
        while True:
            await websocket.send(str(self.queue.get()))
            message = await websocket.recv()
            print("Sent data, got " + message)
            self.queue.task_done()

    def thread_init(self):
        asyncio.run(self.setup())

    async def setup(self):
        async with websockets.serve(self.handler, "localhost", 8000):
            await asyncio.get_running_loop().create_future()

    def broadcast(self, message):
        self.queue.put(json.dumps(message))
        
    def __init__(self):
        self.queue = Queue()
        
        socket_thread = threading.Thread(target=self.thread_init)
        socket_thread.start()
