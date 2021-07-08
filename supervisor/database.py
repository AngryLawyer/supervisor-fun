import aiosqlite

class Database:
    async def start(self):
        self.database = await aiosqlite.connect('database.db') 
        await self.database.execute('''
            CREATE TABLE IF NOT EXISTS
                machines(
                    id TEXT PRIMARY KEY
                )
        ''')
        return self

    async def list_machines(self):
        async with self.database.execute('SELECT id FROM machines') as cursor:
            async for row in cursor:
                print(row)

    async def register(self, identifier):
        pass

