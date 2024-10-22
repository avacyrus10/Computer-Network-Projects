# HTTP/HTTPS Proxy

This project implements an HTTP/HTTPS proxy using Python's `asyncio` library. The proxy listens for client requests, forwards them to the destination server, and relays the server's response back to the client. It supports both HTTP and HTTPS connections and handles multiple requests concurrently.

## Features

1. **Handling both HTTP and HTTPS requests**: The proxy can manage requests using the HTTP and HTTPS protocols.
2. **Asynchronous operation**: The `asyncio` library is used to handle multiple requests concurrently, ensuring that the proxy can efficiently process multiple clients.
3. **Request redirection**: The proxy forwards client requests to the destination server and returns the response back to the client.

## Prerequisites

- **Python 3.9** or higher

## Usage

1. **Install the required dependencies**:
   You can install `asyncio` by running the following command:

   ```bash
   make install
   ```
2. **Start the proxy server: To run the proxy server, use the following command in your terminal**:
```bash
make run
```
  - This will start the proxy server on 127.0.0.1:12345, and it will listen for incoming client requests.
## Code Structure

- main.py: The main entry point for the proxy server. It handles the incoming client connections and delegates the requests to the MyProxy class for processing.
- MyProxy class: Handles both HTTP and HTTPS requests by opening connections to the destination server and relaying data between the client and the server.

## How It Works
1. handle_https:

    - Handles HTTPS requests by establishing a connection to the target server.
    The proxy responds with HTTP/1.1 200 Connection established, then relays the encrypted data between the client and the server.

2. handle_http:

    - Handles HTTP requests by parsing the client's request and forwarding it to the target server.
    The proxy then reads the server's response and sends it back to the client.

3. relay_data:

    - This method relays data between the source (client or server) and the destination, ensuring smooth communication in both directions.

## Example

Server Console Output:
After starting the server with make run, it will listen for incoming requests on 127.0.0.1:12345. For example:
   ``` arduino
Server started on 127.0.0.1:12345
```

Client Console Output:

When a client connects and makes a request, the proxy will process and forward the request to the appropriate destination.

```vbnet
Received client request: GET http://example.com/
Forwarding client request to server: example.com:80
```


