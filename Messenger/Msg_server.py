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
            if user_data.startswith('JO_N'):
                protocol, user_name, user_psw = user_data.split(";")
                user_name_duplicated = msg_db.check_name_duplicate(user_name)
                if user_name_duplicated:
                    print(user_name_duplicated)
                    connection.send('N_ER'.encode())
                    with lock:
                        clients.remove(connection)
                else:
                    # bug should not send to every one with user name
                    msg_to_user = 'J_OK;' + user_name
                    connection.send(msg_to_user.encode())
                    msg_db.add_user_to_db(user_name, user_psw)
            elif user_data.startswith('JOIN'):
                protocol, user_name, user_psw = user_data.split(";")
                result = msg_db.verify_user(user_name, user_psw)
                if result:
                    msg_to_user = 'J_OK;' + user_name
                    connection.send(msg_to_user.encode())
                    msg_db.add_user_to_db(user_name, user_psw)
                else:
                    print("user is not found")
                    messages.put('J_ER')
                    with lock:
                        clients.remove(connection)
            elif user_data.startswith('DATA'):
                protocol, user_name, use_msg = user_data.split(';')
                broadcast_msg = protocol + ';' + user_name + ": " + use_msg
                print(broadcast_msg)
                messages.put(broadcast_msg)
            elif user_data.startswith('EXIT'):
                connection.close()
                with lock:
                    clients.remove(connection)


def broadcast_messages():
    while True:
        if len(clients) > 0:
            broadcast_to_all = str(messages.get()).encode()
            for client in clients:
                client.send(broadcast_to_all)
            print(len(clients))


thread_listen_to_clients = threading.Thread(target=listen_to_clients, args=(mySocket,))
thread_listen_to_clients.start()


thread_broadcast = threading.Thread(target=broadcast_messages)
thread_broadcast.start()


