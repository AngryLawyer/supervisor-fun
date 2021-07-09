from tornado.web import RequestHandler
import json

class MainHandler(RequestHandler):
    def initialize(self, database):
        self.database = database

    async def get(self):
        """for machine in await self.database.list_machines():
            serialized = {
                **machine,
                'registered': machine['registered'].isoformat(),
                'last_updated': machine['last_updated'].isoformat(),
            }
            self.write(json.dumps(serialized))"""
        self.render("index.html")
