class BaseDevice:
    def __init__(self, identifier):
        self.identifier = identifier

    async def think(self):
        raise NotImplementedError()

    def status(self):
        return {
            'id': self.identifier
        }
