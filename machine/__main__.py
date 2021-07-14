from tornado.ioloop import IOLoop
from processor import processor
from devices import get_device
import argparse


def main():
    parser = argparse.ArgumentParser(description='Start a Machine')
    parser.add_argument('identifier', type=str, help='A unique identifier for the machine')
    parser.add_argument('device_type', type=str, help='A device type')
    parser.add_argument('target', type=str, help='The IP address of the supervisor')
    parser.add_argument('port', type=int, help='The port of the supervisor')
    args = parser.parse_args()

    device = get_device(args.device_type)

    async def callback():
        await processor(args.identifier, device, args.target, args.port)

    IOLoop.current().run_sync(callback)

if __name__ == "__main__":
    main()
