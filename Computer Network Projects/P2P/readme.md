# Peer-to-Peer Client-Server Application

This project implements a simple peer-to-peer client-server application using Python's `socket` and `threading` libraries. The server assigns unique IDs to each connected client, and clients can request the IP and port of other clients for direct peer-to-peer communication. The application allows for direct messaging between clients after establishing a connection through the server.

## How It Works

1. **Server**:
   - The server listens for client connections on a specified host and port.
   - It assigns a unique ID to each client and keeps track of connected clients' IP addresses and ports.
   - It sends each new client a list of other connected clients' IDs.
   - Clients can request to connect to another client using their ID, and the server facilitates the connection by providing the requested client's IP address and port.

2. **Client**:
   - A client connects to the server and sends a message.
   - The client receives its unique ID and public IP from the server.
   - The client also receives a list of other connected clients' IDs.
   - The client can choose to connect to another client by specifying their ID.
   - Once connected, the client can send messages directly to the other client.

## Project Structure

- **client.py**: The client-side code that connects to the server, requests other clients' IPs, and establishes direct peer-to-peer connections.
- **server.py**: The server-side code that handles client connections, assigns unique IDs, and facilitates client-to-client communication by sharing IPs and ports.

## How to Run

### 1. Server
To start the server:
1. Run the server script:
   ```bash
   python3 server.py
   ```
2. The client will:
    - Connect to the server.
    - Send a message to the server.
    - Receive a unique ID and public IP.
    - Get a list of other connected clients' IDs.
    - Choose another client to connect to by entering their ID.
    - Establish a direct peer-to-peer connection and send messages.
## Example Interaction

### Server Console Output
- Server starts listening for connections on `127.0.0.1:11112`.
- Server assigns unique IDs to connected clients and prints messages received from clients.

```vbnet
Server listening on 127.0.0.1:11112
Received from ('127.0.0.1', 56789) (ID 1): Hello from client 1
Received from ('127.0.0.1', 56790) (ID 2): Hello from client 2
```
### Client Console Output    
- Client connects to the server and sends a message.
- Client receives its ID and public IP, along with a list of other clients' IDs.
```vbnet
Enter a string: Hello from client 1
Your ID: 1
Your public IP: 127.0.0.1
Other clients' IDs: ['2']
Enter the ID of the client you want to connect to: 2
Sent to other client (ID 2): Hello from client 1 - 2023-11-13 18:09:42.876548
```
### Notes

- The project uses Python's socket library for networking and threading for handling multiple clients concurrently.
- The communication between clients is facilitated by the server, but once the IP and port of the requested client are received, direct peer-to-peer messaging is possible.


