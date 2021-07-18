import json
import logging
from asyncio import wait, create_task, FIRST_COMPLETED
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
from concurrent_handler import ConcurrentHandler
from validation import ValidationException, ActionValidation

logger = logging.getLogger(__name__)


class ProcessorState:
    """
    Base class for a FSM handling the processor's connection
    """

    def __init__(self, remote, port, socket, device):
        logger.info(f"ProcessorState {self.__class__.__name__}")
        self.remote = remote
        self.port = port
        self.socket = socket
        self.device = device

    async def think(self):
        raise NotImplementedError()


class WaitingForConnectionState(ProcessorState):
    """
    The processor has yet to form a connection to the Supervisor

    This state will retry every 5 seconds to form a connection
    """

    async def think(self):
        client = TCPClient()
        try:
            socket = await client.connect(self.remote, self.port)
            return ConnectedState(self.remote, self.port, socket, self.device)
        except (TimeoutError, ConnectionError, StreamClosedError) as e:
            logger.info(f"Failed to phone home - {e}")
        await gen.sleep(5)
        return self


class ConnectedState(ProcessorState):
    """
    The processor has an active connection to the Supervisor

    This state will report the device's status every 5 seconds
    """

    validator = ActionValidation()

    def __init__(self, remote, port, socket, device):
        super().__init__(remote, port, socket, device)
        self.concurrent = ConcurrentHandler(
            {"responder": self.responder, "reader": self.reader}
        )

    async def responder(self):
        self.socket.write(f"{json.dumps(self.device.status())}\n".encode("utf-8"))
        await gen.sleep(5)

    async def reader(self):
        message = await self.socket.read_until(b"\n")
        try:
            data = json.loads(message)
            self.validator.validate(data)
            logger.info(f"Received valid message {data}")
            await self.device.add_message(data)
        except json.JSONDecodeError as e:
            logger.warn(f"Got malformed message {message} from Supervisor - {e}")
        except ValidationException as e:
            logger.warn(f"Message {message} failed to validate - {e}")

    async def think(self):
        try:
            await self.concurrent.process()
        except Exception as ex:
            logger.info(f"Disconnecting due to {ex}")
            return WaitingForConnectionState(self.remote, self.port, None, self.device)
        return self


async def processor(identifier, device_constructor, remote, port):
    """
    Start the main loop of a given machine

    This will process the Device's think method asynchronously
    to reporting it to the server
    """

    device = device_constructor(identifier)
    state = WaitingForConnectionState(remote, port, None, device)

    async def connection():
        nonlocal state
        while True:
            state = await state.think()

    async def device_task():
        nonlocal device
        while True:
            await device.think()

    concurrent = ConcurrentHandler(
        {"connection": connection, "device_task": device_task}
    )

    while True:
        await concurrent.process()
