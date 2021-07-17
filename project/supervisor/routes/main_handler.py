from tornado.web import RequestHandler
import json


class MainHandler(RequestHandler):
    """
    Render the frontend of the system
    """

    async def get(self):
        self.render("index.html")
