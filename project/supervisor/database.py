import aiosqlite
import json
from dateutil import parser


class Database:
    """
    Database routines for the project
    """

    async def start(self, database="database.db"):
        """
        Connect to the database and initialize it, if needed
        """

        self.database = await aiosqlite.connect(database)
        await self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS
                machines(
                    id TEXT PRIMARY KEY NOT NULL,
                    registered TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    last_payload TEXT NOT NULL
                )
        """
        )
        return self

    async def list_machines(self):
        """
        List all of the machines that have ever registered
        with the supervisor
        """

        async with self.database.execute(
            "SELECT id, registered, last_updated, last_payload FROM machines"
        ) as cursor:
            return [
                {
                    "id": id,
                    "registered": parser.parse(registered),
                    "last_updated": parser.parse(last_updated),
                    "last_payload": json.loads(last_payload),
                }
                async for (id, registered, last_updated, last_payload) in cursor
            ]

    async def machine_exists(self, id):
        """
        Check whether a machine of a given ID has ever registered
        """
        async with self.database.execute(
            "SELECT id FROM machines WHERE id = (?)", (id,)
        ) as cursor:
            return await cursor.fetchone() is not None

    async def register(self, payload, datetime):
        """
        Create a new machine with given details
        """

        async with self.database.execute(
            "INSERT INTO machines (id, registered, last_updated, last_payload) VALUES (?,?,?,?)",
            (
                payload["id"],
                f"{datetime.isoformat()}Z",
                f"{datetime.isoformat()}Z",
                json.dumps(payload),
            ),
        ) as cursor:
            await self.database.commit()
            return cursor.lastrowid

    async def update(self, payload, datetime):
        """
        Update a machine with the latest data
        """
        async with self.database.execute(
            "UPDATE machines SET (last_updated, last_payload) = (?,?) WHERE id = (?)",
            (f"{datetime.isoformat()}Z", json.dumps(payload), payload["id"]),
        ) as cursor:

            await self.database.commit()
