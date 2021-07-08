from tornado.web import RequestHandler

class MainHandler(RequestHandler):
    def initialize(self, database):
        self.database = database

    async def get(self):
        await self.database.list_machines()
        self.write("HOWDY")
