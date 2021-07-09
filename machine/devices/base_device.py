class BaseDevice:
    def __init__(self, identifier):
        self.identifier = identifier
        self.template = None

    async def think(self):
        raise NotImplementedError()

    def status(self):
        return {
            'id': self.identifier,
            'template': self.template,
        }
