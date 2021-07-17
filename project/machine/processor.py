import json
from asyncio import wait, create_task, FIRST_COMPLETED
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
from concurrent_handler import ConcurrentHandler

class ProcessorState:
    def __init__(self, remote, port, socket, device):
        print(f'State {self.__class__.__name__}')
        self.remote = remote
        self.port = port
        self.socket = socket
        self.device = device

    async def think(self):
        raise NotImplementedError()


class WaitingForConnectionState(ProcessorState):
    async def think(self):
        client = TCPClient()
        try:
            socket = await client.connect(self.remote, self.port)
            return ConnectedState(self.remote, self.port, socket, self.device)
        except (TimeoutError, ConnectionError, StreamClosedError) as e:
            print(f'Failed to phone home - {e}')
        await gen.sleep(5)
        return self


class ConnectedState(ProcessorState):
    def __init__(self, remote, port, socket, device):
        super().__init__(remote, port, socket, device)
        self.concurrent = ConcurrentHandler({
            "responder": self.responder,
            "reader": self.reader
        })
        self.pending_responder = None
        self.pending_reader = None

    async def responder(self):
        await self.device.think()
        self.socket.write(f'{json.dumps(self.device.status())}\n'.encode('utf-8'))
        await gen.sleep(5)

    async def reader(self):
        message = await self.socket.read_until(b'\n')
        print("OOOH", message)
        # TODO: Validation
        await self.device.add_message(json.loads(message))

    async def think(self):
        try:
            await self.concurrent.process()
        except Exception as ex:
            print(f"Disconnecting due to {ex}")
            return WaitingForConnectionState(self.remote, self.port, None, self.device)
        return self


async def processor(identifier, device_constructor, remote, port):
    device = device_constructor(identifier)
    state = WaitingForConnectionState(remote, port, None, device)
    while True:
        state = await state.think()
