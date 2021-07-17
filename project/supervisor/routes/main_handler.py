from tornado.web import RequestHandler
import json

class MainHandler(RequestHandler):
    async def get(self):
        self.render("index.html")
