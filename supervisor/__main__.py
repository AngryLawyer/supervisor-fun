from tornado.ioloop import IOLoop
from tornado.web import Application
from routes import make_routes
from database import Database
import argparse

def main():
    parser = argparse.ArgumentParser(description='Start a Supervisor')
    parser.add_argument('port', type=int, help='Which port to listen on')
    args = parser.parse_args()

    async def start():
        database = await Database().start()
        app = Application(make_routes(database))
        app.listen(args.port)

    IOLoop.current().add_callback(start)
    IOLoop.current().start()

if __name__ == "__main__":
    main()
