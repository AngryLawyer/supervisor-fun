import json
from asyncio import wait, create_task, FIRST_COMPLETED
from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError

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
        self.pending_responder = None
        self.pending_reader = None

    async def responder(self):
        await self.device.think()
        self.socket.write(f'{json.dumps(self.device.status())}\n'.encode('utf-8'))
        await gen.sleep(5)

    async def reader(self):
        message = await self.socket.read_until('/n')
        # TODO: Validation
        await self.device.add_message(json.loads(message))

    async def think(self):
        responder = self.pending_responder if self.pending_responder is not None else create_task(self.responder(), name="responder")
        reader = self.pending_reader if self.pending_reader is not None else create_task(self.reader(), name="reader")
        self.pending_responder = None
        self.pending_reader = None

        (done, pending) = await wait({responder, reader}, return_when=FIRST_COMPLETED)
        # If one of our tasks has an exception, we probably want to stop
        for item in done:
            ex = item.exception()
            if ex:
                print(f"Disconnecting processor due to {ex}")
                [item.cancel() for item in pending]
                return WaitingForConnectionState(self.remote, self.port, None, self.device)

        # Pop incomplete tasks back in the queue
        for item in pending:
            name = item.get_name()
            if name == "responder":
                self.pending_responder = item
            elif name == "reader":
                self.pending_reader = item
        
        return self


async def processor(identifier, device_constructor, remote, port):
    device = device_constructor(identifier)
    state = WaitingForConnectionState(remote, port, None, device)
    while True:
        state = await state.think()
