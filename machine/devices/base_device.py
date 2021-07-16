from asyncio import Queue

class BaseDevice:
    def __init__(self, identifier):
        self.identifier = identifier
        self.template = None
        self.messages = Queue()

    async def add_message(self, message):
        await self.messages.put(message)

    async def think(self):
        raise NotImplementedError()

    def status(self):
        return {
            'id': self.identifier,
            'template': self.template,
        }
