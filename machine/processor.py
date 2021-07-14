import json
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
    async def think(self):
        await self.device.think()
        try:
            self.socket.write(f'{json.dumps(self.device.status())}\n'.encode('utf-8'))
        except StreamClosedError as e:
            return WaitingForConnectionState(self.remote, self.port, None, self.device)
        await gen.sleep(5)
        return self


async def processor(identifier, device_constructor, remote, port):
    device = device_constructor(identifier)
    state = WaitingForConnectionState(remote, port, None, device)
    while True:
        state = await state.think()
