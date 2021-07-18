from machine.devices.blinker import Blinker
from machine.devices.water_tank import WaterTank


def get_device(name):
    devices = {"Blinker": Blinker, "WaterTank": WaterTank}
    if name in devices:
        return devices[name]
    raise NotImplementedError(
        f'Unknown device {name}. Valid devices are {", ".join(devices.keys())}'
    )
