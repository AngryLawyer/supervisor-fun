from asyncio import Queue, QueueEmpty


class BaseDevice:
    """
    Base class for each Device simulator
    """

    def __init__(self, identifier):
        self.identifier = identifier
        self._template = None
        self._messages = Queue()

    async def add_message(self, message):
        await self._messages.put(message)

    async def think(self):
        """
        Do any processing or mutations this device
        needs to do. This function is called as often as it returns,
        so it's worth sleeping if you want to control timing
        """
        raise NotImplementedError()

    def drain_queue(self):
        """
        Pull all items out of the message queue
        without blocking
        """

        messages = []
        try:
            while True:
                item = self._messages.get_nowait()
                messages.append(item)
        except QueueEmpty:
            pass
        return messages

    def actions(self):
        """
        The list of available commands that
        a frontend is allowed to send
        """

        return []

    def status(self):
        """
        Return basic information about this Device

        Derived classes should add their own information
        to this object
        """

        return {
            "id": self.identifier,
            "template": self._template,
            "actions": self._actions(),
        }
