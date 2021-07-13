from tornado.ioloop import IOLoop
from tornado.web import Application
from routes import make_routes
from database import Database
from callback_server import CallbackServer
import argparse
import os

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "../static"),
}
 
def main():
    parser = argparse.ArgumentParser(description='Start a Supervisor')
    parser.add_argument('http_port', type=int, help='Which port to listen on for HTTP')
    parser.add_argument('tcp_port', type=int, help='Which port to listen on for direct TCP')
    args = parser.parse_args()

    async def start():
        database = await Database().start()
        app = Application(make_routes(database), **settings)
        app.listen(args.http_port)
        callback_server = CallbackServer()
        callback_server.listen(args.tcp_port)

    IOLoop.current().add_callback(start)
    IOLoop.current().start()

if __name__ == "__main__":
    main()
