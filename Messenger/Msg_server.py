import socket
import queue
import threading
import msg_db
import protocol

# storage for messages
messages = queue.Queue()

# storage for clients connection
clients = []

# user name list
users = []

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
            users.remove(user_data.split(';')[1])
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
                server_response = protocol.response_JO_N(user_data, msg_db)

                if server_response.startswith('N_ER'):
                    connection.send(server_response.encode())
                    with lock:
                        clients.remove(connection)
                elif server_response.startswith('J_OK'):
                    connection.send(server_response.encode())
                    users.append(server_response.split(';')[1])
                    all_users = broadcast_user_list()
                    messages.put(all_users)
                    # user_list = 'LIST;' + users
                    # messages.put(users.encode())
                    print(len(users))
                    print(server_response.split(';')[1])

            elif user_data.startswith('JOIN'):
                server_response = protocol.response_JOIN(user_data, msg_db)

                if server_response.startswith('J_OK'):
                    connection.send(server_response.encode())
                    users.append(server_response.split(';')[1])
                    all_users = broadcast_user_list()
                    messages.put(all_users)
                elif server_response.startswith('J_ER'):
                    connection.send(server_response.encode())

            elif user_data.startswith('DATA'):
                broadcast_msg = protocol.response_DATA(user_data)
                messages.put(broadcast_msg)

            elif user_data.startswith('QUIT'):
                connection.send('REMV'.encode())
                # remove from user list here
                # remove connection from error catch part
                #
                # connection.close()
                # with lock:
                #     clients.remove(connection)


def broadcast_user_list():
    all_user = ''
    for user in users:
        all_user += user + ' '
    all_user = 'LIST;' + all_user
    return all_user
    # for client in clients:
    #     client.send(all_user)


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


