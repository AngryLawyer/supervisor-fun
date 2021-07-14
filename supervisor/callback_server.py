from asyncio import Queue
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.ioloop import IOLoop
import json


class CallbackServer(TCPServer):
    def __init__(self, main_queue):
        super().__init__()
        self.main_queue = main_queue
        self.response_queue = Queue()

    def response_message(self, data):
        post = json.loads(data)
        return (post, self.response_queue)

    async def handle_stream(self, stream, address):
        while True:
            try:
                data = await stream.read_until(b"\n")
                # TODO: Validate it's the shape we expect
                await self.main_queue.put(self.response_message(data))
                # await stream.write(data)
            except StreamClosedError:
                break
