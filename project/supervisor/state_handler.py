from asyncio import Queue, create_task, FIRST_COMPLETED, wait
from concurrent_handler import ConcurrentHandler
from datetime import datetime

class StateHandler:
    """
    Track the state of various input handlers,
    and handle passing messages between our TCP links
    and the webserver
    """

    def __init__(self, database):
        self._database = database
        self._handlers = {}
        self.input_queue = Queue()
        self.output_queue = Queue()

    async def _read_from_tcp(self):
        """
        A task to listen to input events from a TCP link

        This updates the database and stores the queues that
        each TCP link gives them
        """
        (payload, reply) = await self.input_queue.get()
        if not await self._database.machine_exists(payload['id']):
            await self._database.register(payload, datetime.utcnow())
        else:
            await self._database.update(payload, datetime.utcnow())
        self._handlers[payload['id']] = reply

    async def _write_to_tcp(self):
        """
        A task that listens for messages to send to specific handlers
        """

        payload = await self.output_queue.get()
        handler = self._handlers.get(payload['id'], None)
        if handler:
            await handler.put(payload)

    async def loop(self):
        """
        Begin an infinite loop to handle passing messages
        between the webserver and individual TCP links
        """
        concurrent = ConcurrentHandler({
            "write_to_tcp": self._write_to_tcp,
            "read_from_tcp": self._read_from_tcp,
        })
        while True:
            await concurrent.process()
