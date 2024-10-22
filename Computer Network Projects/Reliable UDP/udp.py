import socket
import threading
import queue

client_sequence_num = 0
server_sequence_num = 0
client_window_size = 4
server_window_size = 4

client_queue = queue.Queue()
server_queue = queue.Queue()

client_unacked_packets = []
server_unacked_packets = []


def receive_from_client(client_socket):
    global server_sequence_num
    while True:
        data, _ = client_socket.recvfrom(1024)
        client_queue.put((server_sequence_num, data))
        server_sequence_num += 1


def receive_from_server(server_socket):
    global client_sequence_num
    while True:
        data, _ = server_socket.recvfrom(1024)
        server_queue.put((client_sequence_num, data))
        client_sequence_num += 1


def send_to_server(destination_socket):
    global client_sequence_num, client_window_size
    while True:
        while client_sequence_num < len(client_unacked_packets) + client_window_size and not client_queue.empty():
            seq, data = client_queue.get()
            client_unacked_packets.append((seq, data))
            destination_socket.send(data)
            client_sequence_num += 1


def send_to_client(destination_socket):
    global server_sequence_num, server_window_size
    while True:
        while server_sequence_num < len(server_unacked_packets) + server_window_size and not server_queue.empty():
            seq, data = server_queue.get()
            server_unacked_packets.append((seq, data))
            destination_socket.send(data)
            server_sequence_num += 1


def run_my_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('127.0.0.1', 54321))

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as destination_socket:
            destination_socket.connect(('127.0.0.1', 54322))

            client_receiver = threading.Thread(target=receive_from_client, args=(server_socket,))
            server_sender = threading.Thread(target=send_to_client, args=(destination_socket,))

            client_receiver.start()
            server_sender.start()

            client_receiver.join()
            server_sender.join()


def run_my_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.bind(('127.0.0.1', 1111))

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as destination_socket:
            destination_socket.connect(('127.0.0.1', 12345))

            server_receiver = threading.Thread(target=receive_from_server, args=(client_socket,))
            client_sender = threading.Thread(target=send_to_server, args=(destination_socket,))

            server_receiver.start()
            client_sender.start()

            server_receiver.join()
            client_sender.join()


if __name__ == "__main__":
    intermediary_server = threading.Thread(target=run_my_server)
    intermediary_client = threading.Thread(target=run_my_client)

    intermediary_server.start()
    intermediary_client.start()

    intermediary_server.join()
    intermediary_client.join()
