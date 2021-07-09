from tornado.web import RequestHandler
from datetime import datetime
import json

class CallbackHandler(RequestHandler):
    def initialize(self, database):
        self.database = database

    async def post(self):
        post = json.loads(self.request.body)
        # TODO: Validate inputs
        if not await self.database.machine_exists(post['id']):
            await self.database.register(post, datetime.utcnow())
        else:
            await self.database.update(post, datetime.utcnow())
        self.set_status(204) # NO_CONTENT
