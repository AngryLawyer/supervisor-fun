import json
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

async def processor(identifier, device_constructor, remote):
    client = AsyncHTTPClient()
    device = device_constructor(identifier)
    while True:
        await device.think()
        try:
            await client.fetch(HTTPRequest(url=remote, method='POST', body=json.dumps(device.status())))
        except (HTTPError, ConnectionError) as e:
            print(f'Failed to phone home - {e}')
        await gen.sleep(5)
