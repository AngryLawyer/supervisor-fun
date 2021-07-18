from tornado import gen
from machine.devices.base_device import BaseDevice
from machine.actions import action
from random import randint
import logging


logger = logging.getLogger(__name__)

REFILL = "refill"


class WaterTankState:
    """
    FSM to track what state the water tank is in
    """

    def __init__(self):
        logger.info(f"Water Tank State {self.__class__.__name__}")

    async def think(self, water_tank):
        raise NotImplementedError()


class DrainingState(WaterTankState):
    """
    The water tank has water, and is currently
    draining at a randomly specified speed
    """

    def __init__(self):
        # Randomly pick a demand level
        super().__init__()
        self.demand_level = randint(1, 10)
        logger.info(f"Water demand is {self.demand_level} units every 5 seconds")

    def think(self, water_tank):
        for message in water_tank.drain_queue():
            if message["action"] == REFILL:
                return FillingState()

        # Water slowly drains from the tank
        if water_tank.water_level > 0:
            water_tank.water_level = max(water_tank.water_level - self.demand_level, 0)
            logger.info(f"Water level drained to {water_tank.water_level}")
        else:
            return EmptyState()
        return self


class EmptyState(WaterTankState):
    """
    The water tank is empty
    """

    def think(self, water_tank):
        for message in water_tank.drain_queue():
            if message["action"] == REFILL:
                return FillingState()
        return self


class FillingState(WaterTankState):
    """
    The water tank is currently filling
    """

    def think(self, water_tank):
        water_tank.drain_queue()  # Discard all messages, you can't do anything while filling

        # Water refills much quicker
        if water_tank.water_level < 100:
            water_tank.water_level = min(water_tank.water_level + 10, 100)
            logger.info(f"Water level filled to {water_tank.water_level}")
        else:
            return DrainingState()
        return self


class WaterTank(BaseDevice):
    """
    A simulated water tank.

    Water will drain from the tank at a randomly
    determined speed, until empty.
    The water level can be refilled by sending it
    a REFILL message
    """

    def __init__(self, identifier):
        super().__init__(identifier)
        self.template = "water_tank"
        self.water_level = 100
        self.state = DrainingState()

    async def think(self):
        self.state = self.state.think(self)
        await gen.sleep(5)

    def status(self):
        return {
            **super().status(),
            "water_level": self.water_level,
        }

    def actions(self):
        if self.state.__class__ != FillingState:
            return [*super().actions(), action(REFILL, "Refill")]
        return super().actions()
