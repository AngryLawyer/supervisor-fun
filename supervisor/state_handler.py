from asyncio import Queue

class StateHandler:
    def __init__(self):
        self.handlers = {}
        self.input_queue = Queue()

    async def loop(self):
        while True:
            item = await self.input_queue.get()
            print(item)
