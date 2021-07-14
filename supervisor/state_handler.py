from asyncio import Queue
from datetime import datetime

class StateHandler:
    def __init__(self, database):
        self.database = database
        self.handlers = {}
        self.input_queue = Queue()

    async def loop(self):
        while True:
            (payload, reply) = await self.input_queue.get()
            if not await self.database.machine_exists(payload['id']):
                await self.database.register(payload, datetime.utcnow())
            else:
                await self.database.update(payload, datetime.utcnow())
            self.handlers[payload['id']] = reply
            print(payload)
