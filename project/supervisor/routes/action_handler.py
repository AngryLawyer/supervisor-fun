from tornado.web import RequestHandler
from tornado.escape import url_unescape
from datetime import datetime
import json


class ActionHandler(RequestHandler):
    """
    Handle the frontend sending commands to
    an individual Machine
    """

    def initialize(self, queue):
        self.queue = queue

    async def post(self, service_name):
        # TODO: Validate the message
        body = json.loads(self.request.body)
        await self.queue.put({**body, "id": url_unescape(service_name)})
        self.set_status(204)  # NO CONTENT
