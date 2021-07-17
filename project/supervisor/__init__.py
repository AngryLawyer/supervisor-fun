from tornado.ioloop import IOLoop
from tornado.web import Application
from supervisor.routes import make_routes
from supervisor.database import Database
from supervisor.callback_server import CallbackServer
from supervisor.state_handler import StateHandler
import argparse
import os

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "../static"),
}


def add_supervisor_subparser(subparsers):
    parser = subparsers.add_parser(name="supervisor", description="Start a supervisor")
    parser.add_argument('http_port', type=int, help='Which port to listen on for HTTP')
    parser.add_argument('tcp_port', type=int, help='Which port to listen on for direct TCP')
    parser.set_defaults(func=main)
 
def main():
    async def start():
        database = await Database().start()
        state_handler = StateHandler(database)
        IOLoop.current().add_callback(state_handler.loop)
        app = Application(make_routes(database, state_handler.output_queue), **settings)
        app.listen(args.http_port)
        callback_server = CallbackServer(state_handler.input_queue)
        callback_server.listen(args.tcp_port)

    IOLoop.current().add_callback(start)
    IOLoop.current().start()
