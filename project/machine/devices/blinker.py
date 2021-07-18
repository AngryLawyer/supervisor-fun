from tornado import gen
from machine.devices.base_device import BaseDevice


class Blinker(BaseDevice):
    """
    A simple light that toggles on and off
    every 5 seconds
    """

    state = False

    def __init__(self, identifier):
        super().__init__(identifier)
        self.template = 'light'


    async def think(self):
        self.state = not self.state
        await gen.sleep(5)


    def status(self):
        return {
            **super().status(),
            'power': self.state,
        }
