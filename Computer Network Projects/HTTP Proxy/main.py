import asyncio
from proxy import MyProxy
import sys


async def start_connection():
    host = '127.0.0.1'
    port = 12345

    try:
        server = await asyncio.start_server(
            handle_client, host, port
        )

        async with server:
            await server.serve_forever()
    except Exception as e:
        print("Failed to initialize socket:", e)
        sys.exit(2)


async def handle_client(reader, writer):
    data = await reader.read(8192)
    p = MyProxy(reader, writer, data)
    await p.handle_request()


if __name__ == '__main__':
    asyncio.run(start_connection())
