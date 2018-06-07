import socket
import queue
import threading

# storage for messages
messages = queue.Queue()

# storage for clients
clients = []

# set TCP/IP server
HOST = '127.0.0.1'
PORT = 3000
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((HOST, PORT))
mySocket.listen(1)


def listen_to_clients(sock):
    while True:
        try:
            print("Waiting for connection...")
            conn, addr = sock.accept()
            print("A client is connected")
            clients.append(conn)
            thread_new_client = threading.Thread(target=client_handler, args=(conn, messages))
            thread_new_client.start()
        except ConnectionResetError:
            print("connection reset error")
            continue


def client_handler(connection, messages):
    while True:
        user_data = connection.recv(1024).decode()
        print(user_data)
        if user_data.startswith('data'):
            messages.put(user_data)
        elif user_data.startswith('EXIT'):
            connection.close()


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


