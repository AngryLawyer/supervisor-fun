from devices.base_device import BaseDevice

class WaterTank(BaseDevice):
    def __init__(self, identifier):
        super().__init__(identifier)
        self.template = 'water_tank'
        self.water_level = 1.0

    async def think(self):
        # Water slowly drains from the tank
        if self.water_level > 0.0:
            self.water_level -= 0.01

    def status(self):
        return {
            **super().status(),
            "water_level": self.water_level,
        }
