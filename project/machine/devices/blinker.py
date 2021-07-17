from machine.devices.base_device import BaseDevice

class Blinker(BaseDevice):
    state = False

    def __init__(self, identifier):
        super().__init__(identifier)
        self.template = 'light'

    async def think(self):
        self.state = not self.state

    def status(self):
        return {
            **super().status(),
            'power': self.state,
        }