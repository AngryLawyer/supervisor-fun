from tornado.ioloop import IOLoop
from processor import processor
from devices import get_device
import argparse


def main():
    parser = argparse.ArgumentParser(description='Start a Machine')
    parser.add_argument('identifier', type=str, help='A unique identifier for the machine')
    parser.add_argument('device_type', type=str, help='A device type')
    parser.add_argument('target', type=str, help='An IP address and port of a supervisor')
    args = parser.parse_args()

    device = get_device(args.device_type)

    async def callback():
        await processor(args.identifier, device, args.target)

    IOLoop.current().run_sync(callback)

if __name__ == "__main__":
    main()
