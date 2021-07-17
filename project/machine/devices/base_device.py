from asyncio import Queue, QueueEmpty

class BaseDevice:
    def __init__(self, identifier):
        self.identifier = identifier
        self.template = None
        self.messages = Queue()

    async def add_message(self, message):
        await self.messages.put(message)

    async def think(self):
        raise NotImplementedError()

    def drain_queue(self):
        messages = []
        try:
            while True:
                item = self.messages.get_nowait()
                messages.append(item)
        except QueueEmpty:
            pass
        return messages

    def actions(self):
        return []

    def status(self):
        return {
            'id': self.identifier,
            'template': self.template,
            'actions': self.actions(),
        }
