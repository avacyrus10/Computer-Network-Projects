import asyncio
import socket


class MyProxy:
    def __init__(self, reader, writer, data):
        self.reader = reader
        self.writer = writer
        self.data = data

    async def handle_request(self):
        try:
            first_line = self.data.split(b'\n')[0].decode()
            method = first_line.split(' ')[0]

            if method == "CONNECT":
                await self.handle_https()
            else:
                await self.handle_http()

        except Exception as e:
            print("Error handling request:", e)

    async def handle_https(self):
        try:

            host, port = self.data.split(b' ')[1].split(b':')
            port = int(port)

            reader, writer = await asyncio.open_connection(host.decode(), port)

            response = b"HTTP/1.1 200 Connection established\r\n\r\n"
            self.writer.write(response)
            await self.writer.drain()

            await asyncio.gather(
                self.relay_data(self.reader, writer),
                self.relay_data(reader, self.writer)
            )

        except Exception as e:
            print("Error handling HTTPS request:", e)

    async def handle_http(self):
        try:
            first_line = self.data.split(b'\n')[0].decode()
            url = first_line.split(' ')[1]
            http_pos = url.find('://')
            if http_pos == -1:
                temp = url
            else:
                temp = url[http_pos + 3:]

            port_pos = temp.find(":")
            web_server_pos = temp.find("/")
            if web_server_pos == -1:
                web_server_pos = len(temp)

            web_server = ""
            port = -1
            if port_pos == -1 or web_server_pos < port_pos:
                port = 80
                web_server = temp[:web_server_pos]
            else:
                port = int((temp[port_pos + 1:])[:web_server_pos - port_pos - 1])
                web_server = temp[:port_pos]

            reader, writer = await asyncio.open_connection(web_server, port)

            writer.write(self.data)
            await writer.drain()

            await asyncio.gather(
                self.relay_data(reader, self.writer),
                self.relay_data(self.reader, writer)
            )

        except Exception as e:
            print("Error handling HTTP request:", e)

    async def relay_data(self, source, destination):
        try:
            while True:
                data = await source.read(8192)
                if data:
                    destination.write(data)
                    await destination.drain()
                else:
                    break
        except Exception as e:
            print("Error relaying data:", e)
        finally:
            if not source.at_eof():
                source.feed_eof()

            if isinstance(destination, asyncio.StreamWriter) and not destination.is_closing():
                destination.close()
