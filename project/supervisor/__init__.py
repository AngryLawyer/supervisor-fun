from tornado.ioloop import IOLoop
from tornado.web import Application
from supervisor.routes import make_routes
from supervisor.database import Database
from supervisor.callback_server import CallbackServer
from supervisor.state_handler import StateHandler
import argparse
import os
import logging

logger = logging.getLogger(__name__)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "../../static"),
}


def add_supervisor_subparser(subparsers):
    parser = subparsers.add_parser(name="supervisor", description="Start a supervisor")
    parser.add_argument("http_port", type=int, help="Which port to listen on for HTTP")
    parser.add_argument(
        "tcp_port", type=int, help="Which port to listen on for direct TCP"
    )
    parser.set_defaults(func=main)


def main(args):
    """
    Start up the supervisor, including webserver and TCP handler
    """

    async def start():
        logger.info("Starting database...")
        database = await Database().start()
        state_handler = StateHandler(database)
        app = Application(make_routes(database, state_handler.output_queue), **settings)
        logger.info("Starting webserver...")
        app.listen(args.http_port)
        logger.info("Starting tcp callback server...")
        callback_server = CallbackServer(state_handler.input_queue)
        callback_server.listen(args.tcp_port)
        logger.info("Starting state handling loop")
        await state_handler.loop()

    IOLoop.current().add_callback(start)
    IOLoop.current().start()
