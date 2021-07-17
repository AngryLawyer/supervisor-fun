import aiosqlite
import json
from dateutil import parser

class Database:
    async def start(self):
        self.database = await aiosqlite.connect('database.db') 
        await self.database.execute('''
            CREATE TABLE IF NOT EXISTS
                machines(
                    id TEXT PRIMARY KEY NOT NULL,
                    registered TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    last_payload TEXT NOT NULL
                )
        ''')
        return self

    async def list_machines(self):
        out = []
        async with self.database.execute('SELECT id, registered, last_updated, last_payload FROM machines') as cursor:
            async for (id,registered,last_updated,last_payload) in cursor:
                out.append({
                    'id': id,
                    'registered': parser.parse(registered),
                    'last_updated': parser.parse(last_updated),
                    'last_payload': json.loads(last_payload)
                })
        return out

    async def machine_exists(self, id):
        async with self.database.execute('SELECT id FROM machines WHERE id = (?)', (id,)) as cursor:
            return (await cursor.fetchone() is not None)

    async def register(self, payload, datetime):
        async with self.database.execute('INSERT INTO machines (id, registered, last_updated, last_payload) VALUES (?,?,?,?)', (payload['id'], f'{datetime.isoformat()}Z', f'{datetime.isoformat()}Z', json.dumps(payload))) as cursor:
            await self.database.commit()
            return cursor.lastrowid

    async def update(self, payload, datetime):
        async with self.database.execute('UPDATE machines SET (last_updated, last_payload) = (?,?) WHERE id = (?)', (f'{datetime.isoformat()}Z', json.dumps(payload), payload['id'])) as cursor:
            await self.database.commit()
