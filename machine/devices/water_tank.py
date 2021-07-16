from devices.base_device import BaseDevice
from actions import action
from random import randint

REFILL = 'refill'

class WaterTankState:
    def __init__(self):
        print(f'Water Tank State {self.__class__.__name__}')

    async def think(self, water_tank):
        raise NotImplementedError()

class DrainingState(WaterTankState):
    def __init__(self):
        # Randomly pick a demand level
        super().__init__()
        self.demand_level = randint(1, 10)

    def think(self, water_tank):
        for message in water_tank.drain_queue():
            if message['action'] == REFILL:
                return FillingState()

        # Water slowly drains from the tank
        if water_tank.water_level > 0:
            water_tank.water_level = max(water_tank.water_level - self.demand_level, 0)
        else:
            return EmptyState()
        return self


class EmptyState(WaterTankState):
    def think(self, water_tank):
        for message in water_tank.drain_queue():
            if message['action'] == REFILL:
                return FillingState()
        return self


class FillingState(WaterTankState):
    def think(self, water_tank):
        water_tank.drain_queue() # Discard all messages, you can't do anything while filling

        # Water refills much quicker
        if water_tank.water_level < 100:
            water_tank.water_level = min(water_tank.water_level + 10, 100)
        else:
            return DrainingState()
        return self


class WaterTank(BaseDevice):
    def __init__(self, identifier):
        super().__init__(identifier)
        self.template = 'water_tank'
        self.water_level = 100
        self.state = DrainingState()

    async def think(self):
        self.state = self.state.think(self)

    def status(self):
        return {
            **super().status(),
            "water_level": self.water_level,
        }

    def actions(self):
        if self.state.__class__ != FillingState:
            return [
                *super().actions(),
                action(REFILL, "Refill")
            ]
        return super().actions()
