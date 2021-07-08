from devices.blinker import Blinker

def get_device(name):
    devices = {
        'Blinker': Blinker
    }
    if name in devices:
        return devices[name]
    raise NotImplementedError(f'Unknown device {name}. Valid devices are {", ".join(devices.keys())}')
