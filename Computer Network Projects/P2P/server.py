import socket
import threading

clients = {}
client_count = 0


def handle_client_messages(client_socket, addr, client_id):
    '''
    This function checks the receiving messages from clients and if the message starts with connect
    it means that a client has requested to connect to another client, thus the IP and port of the
    requested client will be sent back to it.
    '''
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')

            if message.startswith("connect"):
                requested_id = int(message.split()[1])

                if requested_id in clients:
                    requested_client_socket, requested_client_addr = clients[requested_id]
                    client_socket.send(f"{requested_client_addr[0]}:{requested_client_addr[1]}".encode('utf-8'))
                else:
                    client_socket.send("Invalid client ID".encode('utf-8'))

            elif not message:
                break

            print(f"Received from {addr} (ID {client_id}): {message}")

    except Exception as e:
        print(f"Error handling messages from {addr}: {e}")
    finally:
        del clients[client_id]
        client_socket.close()


def accept_clients(server_socket):
    '''
    here in this function an ID will be assigned to each new client
    and their messages will be shown and all the available clients
    and their equivalent IDs will be sent to the new arriving clients.
    '''
    global client_count
    while True:
        try:
            client_socket, addr = server_socket.accept()

            client_count += 1
            client_id = client_count

            input_string = client_socket.recv(1024).decode('utf-8')
            print(f"Received from {addr} (ID {client_id}): {input_string}")

            client_socket.send(str(client_id).encode('utf-8'))
            client_socket.send(str(addr[0]).encode('utf-8'))

            clients[client_id] = (client_socket, addr)

            other_clients_ids = [str(other_client_id) for other_client_id in clients if other_client_id != client_id]
            client_socket.send(','.join(other_clients_ids).encode('utf-8'))

            threading.Thread(target=handle_client_messages, args=(client_socket, addr, client_id)).start()

        except Exception as e:
            print(f"Error accepting connection from client: {e}")


def main():
    host = '127.0.0.1'
    port = 11112

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    threading.Thread(target=accept_clients, args=(server_socket,)).start()

    while True:
        pass


if __name__ == "__main__":
    main()

