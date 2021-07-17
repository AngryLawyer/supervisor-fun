from asyncio import Queue, wait, FIRST_COMPLETED, create_task
from concurrent_handler import ConcurrentHandler
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.ioloop import IOLoop
import json


class CallbackServer(TCPServer):
    def __init__(self, main_queue):
        super().__init__()
        self.main_queue = main_queue

    async def handle_stream(self, stream, address):
        def response_message( data):
            post = json.loads(data)
            return (post, response_queue)

        response_queue = Queue()
        async def read_input():
            data = await stream.read_until(b"\n")
            # TODO: Validate it's the shape we expect
            await self.main_queue.put(response_message(data))
            # await stream.write(data)

        async def read_server():
            data = await response_queue.get()
            print("OH NO", data)
            await stream.write(f"{json.dumps(data)}\n".encode('utf-8'))

        concurrent = ConcurrentHandler({
            "input": read_input,
            "server": read_server
        })

        while True:
            await concurrent.process()
