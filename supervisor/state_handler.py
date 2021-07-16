from asyncio import Queue, create_task, FIRST_COMPLETED, wait
from datetime import datetime

class StateHandler:
    def __init__(self, database):
        self.database = database
        self.handlers = {}
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.pending_output = None
        self.pending_input = None

    async def input(self):
        (payload, reply) = await self.input_queue.get()
        if not await self.database.machine_exists(payload['id']):
            await self.database.register(payload, datetime.utcnow())
        else:
            await self.database.update(payload, datetime.utcnow())
        # FIXME: this seems to hold on to dead handlers
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
        while True:
            output = self.pending_output if self.pending_output is not None else create_task(self.output(), name="output")
            input = self.pending_input if self.pending_input is not None else create_task(self.input(), name="input")
            self.pending_output = None
            self.pending_input = None

            # TODO: Abstract this
            (done, pending) = await wait({output, input}, return_when=FIRST_COMPLETED)
            # If one of our tasks has an exception, we probably want to stop
            for item in done:
                # TODO: a Handler exception is non-fatal
                ex = item.exception()
                if ex:
                    print(f"Disconnecting state handler due to {ex}")
                    [item.cancel() for item in pending]
                    return

            # Pop incomplete tasks back in the queue
            for item in pending:
                name = item.get_name()
                if name == "output":
                    self.pending_output = item
                elif name == "input":
                    self.pending_input = item
