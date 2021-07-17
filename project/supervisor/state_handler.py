from asyncio import Queue, create_task, FIRST_COMPLETED, wait
from concurrent_handler import ConcurrentHandler
from datetime import datetime

class StateHandler:
    def __init__(self, database):
        self.database = database
        self.handlers = {}
        self.input_queue = Queue()
        self.output_queue = Queue()

    async def input(self):
        (payload, reply) = await self.input_queue.get()
        if not await self.database.machine_exists(payload['id']):
            await self.database.register(payload, datetime.utcnow())
        else:
            await self.database.update(payload, datetime.utcnow())
        self.handlers[payload['id']] = reply
        print(self.handlers)
        print(payload)

    async def output(self):
        payload = await self.output_queue.get()
        handler = self.handlers.get(payload['id'], None)
        print(handler)
        if handler:
            await handler.put(payload)

    async def loop(self):
        concurrent = ConcurrentHandler({
            "output": self.output,
            "input": self.input,
        })
        while True:
            await concurrent.process()
