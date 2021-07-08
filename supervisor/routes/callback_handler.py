from tornado.web import RequestHandler
import json

class CallbackHandler(RequestHandler):
    def initialize(self, database):
        self.database = database

    def post(self):
        print(json.loads(self.request.body))
        self.write("CALLBACK")
