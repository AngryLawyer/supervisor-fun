from asyncio import Queue, wait, FIRST_COMPLETED, create_task
from concurrent_handler import ConcurrentHandler
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.ioloop import IOLoop
from validation import ValidationException, MachineReportValidation
import json
import logging

logger = logging.getLogger(__name__)


class CallbackServer(TCPServer):
    """
    Open a TCP listener and wait for Machines to connect to us
    """

    validator = MachineReportValidation()

    def __init__(self, main_queue):
        super().__init__()
        self.main_queue = main_queue

    async def handle_stream(self, stream, address):
        """
        Handle a connected TCP address
        """
        logger.info(f"New connection from {address}")

        response_queue = Queue()

        async def read_input():
            message = await stream.read_until(b"\n")
            try:
                data = json.loads(message)
                self.validator.validate(data)
                logger.info(f"Received valid message {data} from {address}")
                await self.main_queue.put((data, response_queue))
            except json.JSONDecodeError as e:
                logger.warn(
                    f"Got malformed message {message} from Machine {address} - {e}"
                )
            except ValidationException as e:
                logger.warn(
                    f"Message {message} failed to validate from Machine {address} - {e}"
                )

        async def read_server():
            data = await response_queue.get()
            logger.info(f"Server dispatching message {data} to {address}")
            await stream.write(f"{json.dumps(data)}\n".encode("utf-8"))

        concurrent = ConcurrentHandler({"input": read_input, "server": read_server})

        while True:
            try:
                await concurrent.process()
            except Exception as e:
                logger.info(f"Exiting tcp callback for {address}: {e}")
                return
