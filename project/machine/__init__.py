from tornado.ioloop import IOLoop
from machine.processor import processor
from machine.devices import get_device
import logging

logger = logging.getLogger(__name__)


def add_machine_subparser(subparsers):
    parser = subparsers.add_parser(name="machine", description="Start a machine")
    parser.add_argument(
        "identifier", type=str, help="A unique identifier for the machine"
    )
    parser.add_argument("device_type", type=str, help="A device type")
    parser.add_argument("target", type=str, help="The IP address of the supervisor")
    parser.add_argument("port", type=int, help="The port of the supervisor")
    parser.set_defaults(func=main)


def main(args):
    """
    Start up an individual machine that will try to connect to the Supervisor
    """

    device = get_device(args.device_type)

    async def callback():
        logger.info(f"Starting Machine with device {device.__class__.__name__}")
        await processor(args.identifier, device, args.target, args.port)

    IOLoop.current().run_sync(callback)
