import socket
from datetime import datetime
import time


def main():
    '''

    First the client will send a message to server and then the server will send
    the public IP of the client. we also receive other clients IDs and we can choose
    to connect to them.
    after requesting to connect we will receive the requested IP and port
    thus we can make a direct connection to the client and send the input message
    to it.
    '''
    server_host = '127.0.0.1'
    server_port = 11112

    user_input = input("Enter a string: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_host, server_port))

        client_socket.send(user_input.encode('utf-8'))

        client_id = int(client_socket.recv(1024).decode('utf-8'))
        print(f"Your ID: {client_id}")

        own_ip = client_socket.recv(1024).decode('utf-8')
        print(f"Your public IP: {own_ip}")

        other_clients_ids = client_socket.recv(1024).decode('utf-8').split(',')
        print("Other clients' IDs:", other_clients_ids)

        requested_id = int(input("Enter the ID of the client you want to connect to: "))
        if requested_id in list(map(int, other_clients_ids)):
            r = f"connect {requested_id}"
            client_socket.send(r.encode('utf-8'))

            other_ip_and_port = client_socket.recv(1024).decode('utf-8')
            other_ip, other_port = other_ip_and_port.split(':')
            other_port = int(other_port)

            direct_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            time.sleep(2)
            print(other_ip)
            print(other_port)
            direct_socket.connect((other_ip, other_port))

            while True:
                message = f"{user_input} - {datetime.now()}"
                direct_socket.send(message.encode('utf-8'))
                print(f"Sent to other client (ID {requested_id}): {message}")

        else:
            print(f"Invalid client ID: {requested_id}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()

