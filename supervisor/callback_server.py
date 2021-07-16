from asyncio import Queue, wait, FIRST_COMPLETED, create_task
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

        pending_input = None
        pending_server = None

        while True:
            pending_input = None
            pending_server = None
            (done, pending) = await wait([pending_input if pending_input is not None else create_task(read_input(), name="input"), pending_server if pending_server else create_task(read_server(), name="server")], return_when=FIRST_COMPLETED)
            # If one of our tasks has an exception, we probably want to stop
            for item in done:
                ex = item.exception()
                if ex:
                    print(f"Exiting callback due to {ex}")
                    return

            # Get our existing messages ready to requeue
            for item in pending:
                name = item.get_name()
                if name == "input":
                    pending_input = item
                elif name == "server":
                    pending_server = item
