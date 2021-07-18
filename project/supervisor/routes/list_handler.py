from tornado.web import RequestHandler
from datetime import datetime
import json


class ListHandler(RequestHandler):
    """
    Return a list of JSON-formatted Machines
    that have registered with the Supervisor
    """

    def initialize(self, database):
        self.database = database

    async def get(self):
        data = await self.database.list_machines()
        self.set_header("Content-Type", "application/json")
        # Python can't automatically serialize date fields,
        # so we do it ourself
        self.write(
            json.dumps(
                [
                    {
                        **row,
                        "registered": row["registered"].isoformat(),
                        "last_updated": row["last_updated"].isoformat(),
                    }
                    for row in data
                ]
            )
        )
