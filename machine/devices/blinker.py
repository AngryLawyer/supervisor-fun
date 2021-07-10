from devices.base_device import BaseDevice

class Blinker(BaseDevice):
    state = False

    async def think(self):
        self.state = not self.state

    def status(self):
        return {
            **super().status(),
            'power': self.state
        }
