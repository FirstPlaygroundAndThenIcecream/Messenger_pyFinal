import socket
import queue
import threading
import msg_db

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

lock = threading.Lock()


def listen_to_clients(sock):
    while True:
        try:
            print("Waiting for connection...")
            conn, addr = sock.accept()
            print("A client is connected")
        except ConnectionResetError:
            print("connection reset error")
        except OSError:
            print("OS error")
        else:
            clients.append(conn)
            thread_new_client = threading.Thread(target=client_handler, args=(conn, messages))
            thread_new_client.start()
            thread_total = threading.active_count()
            print('{:d} threads are running on the server side'.format(thread_total))


def client_handler(connection, messages):
    while True:
        try:
            user_data = connection.recv(1024).decode()
            print(user_data)
        except ConnectionResetError:
            print("A client has dropped connection")
            with lock:
                clients.remove(connection)
            break
        except ConnectionAbortedError:
            print("Unexpected lost connection")
            with lock:
                clients.remove(connection)
            break
        except OSError:
            print("A client has quit")
            break
        except RuntimeError:
            print("runtime error")
            with lock:
                clients.remove(connection)
            break
        else:
            if user_data.startswith('JOIN'):
                protocol, user_name, user_psw = user_data.split(";")
                messages.put('J_OK')
                msg_db.add_user_to_db(user_name, user_psw)
            elif user_data.startswith('DATA'):
                messages.put(user_data)
            elif user_data.startswith('EXIT'):
                connection.close()
                with lock:
                    clients.remove(connection)


def broadcast_messages():
    while True:
        if len(clients) > 0:
            broadcast_to_all = str(messages.get()).encode()
            #with lock:
            for client in clients:
                client.send(broadcast_to_all)


thread_listen_to_clients = threading.Thread(target=listen_to_clients, args=(mySocket,))
thread_listen_to_clients.start()


thread_broadcast = threading.Thread(target=broadcast_messages)
thread_broadcast.start()


