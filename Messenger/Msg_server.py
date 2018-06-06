import socket
import queue
import threading

# storage for messages
messages = queue.Queue()

# storage for clients
clients = []

# set server
host = "127.0.0.1"
port = 3000
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((host, port))
mySocket.listen(5)


def listen_to_clients(socket):
    while True:
        conn, addr = socket.accept()
        clients.append(conn)
        thread_new_client = threading.Thread(target=client_handler, args=(conn, messages))
        thread_new_client.start()


def client_handler(connection):
    while True:
        user_data = connection.recv(2048).decode()
        if user_data.startswith('data'):
            messages.put(user_data)


def broadcast_messages():
    while True:
        if len(clients) > 0:
            broadcast_to_all = str(messages.get()).encode()
            for client in clients:
                client.send(broadcast_to_all)


thread_listen_to_clients = threading.Thread(target=listen_to_clients, args=(mySocket,))
thread_listen_to_clients.start()


thread_broadcast = threading.Thread(target=broadcast_messages)
thread_broadcast.start()


