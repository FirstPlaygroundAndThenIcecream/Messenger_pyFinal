import socket
import queue
import threading
from os import path
from time import gmtime, strftime
import msg_db
import protocol
import User

# storage for messages
exchange_messages = queue.Queue()

# storage for clients connection
clients = []

# user list
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
            thread_new_client = threading.Thread(target=client_handler, args=(conn, exchange_messages))
            thread_new_client.start()
            # thread_total = threading.active_count()
            # print('{:d} threads are running on the server side'.format(thread_total))


def client_handler(connection, messages):
    while True:
        try:
            user_data = ''
            user_data = connection.recv(1024).decode()
        except (ConnectionResetError, UnboundLocalError):
            print("A client has dropped connection")
            if len(user_data) > 0:
                user_name = user_data.split(';')[1]
                remove_user(user_name)
            visible_users = get_visible_users()
            messages.put(visible_users)
            with lock:
                clients.remove(connection)
            break
        except (ConnectionAbortedError, UnboundLocalError):
            print("Unexpected lost connection")
            with lock:
                clients.remove(connection)
            break
        except (OSError, UnboundLocalError):
            print("A client has quit")
            break
        except RuntimeError:
            print("runtime error")
            with lock:
                clients.remove(connection)
            break
        else:
            user_name = user_data.split(';')[1]
            print(user_data)
            if user_data.startswith('JO_N'):
                server_response = protocol.response_JO_N(user_data, msg_db)

                if server_response.startswith('N_ER'):
                        connection.send(server_response.encode())
                elif server_response.startswith('J_OK'):
                        connection.send(server_response.encode())
                        print(user_name + ' has joined')
                        make_user(user_name, connection)
                        print('{} users are online.'.format(len(users)))
                        # sending user list 'LIST;'
                        visible_users = get_visible_users()
                        messages.put(visible_users)
                        print(visible_users)

            elif user_data.startswith('JOIN'):
                server_response = protocol.response_JOIN(user_data, msg_db)

                if server_response.startswith('J_OK'):
                    connection.send(server_response.encode())
                    print(user_name + ' has joined')
                    make_user(user_name, connection)
                    print('{} users are online.'.format(len(users)))
                    visible_users = get_visible_users()
                    messages.put(visible_users)
                    print(visible_users)
                elif server_response.startswith('J_ER'):
                    connection.send(server_response.encode())

            elif user_data.startswith('DATA'):
                broadcast_msg = protocol.response_DATA(user_data)
                messages.put(broadcast_msg)
                print(broadcast_msg.strip())
                log_chat_history(broadcast_msg.split(';')[1])

            elif user_data.startswith('QUIT'):
                set_user_invisible(user_name)
                visible_users = get_visible_users()
                messages.put(visible_users)
                connection.send('REMV'.encode())


def make_user(name, connection):
    user = User.User(name, connection)
    users.append(user)


def remove_user(name):
    for user in users:
        if name == user.get_name():
            users.remove(user)


def set_user_invisible(name):
    for user in users:
        if name == user.get_name():
            user.set_visible(False)


def get_visible_users():
    visible_users = ''
    if len(users) > 0:
        for user in users:
            if user.is_visible() is True:
                visible_users += user.get_name() + ' '
        visible_users = 'LIST;' + visible_users
    return visible_users


def log_chat_history(chat):
    file_name = 'chat_history.txt'
    file_exists = str(path.exists(file_name))
    time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if file_exists == 'False':
        file = open(file_name, 'w+')
    file = open(file_name, 'a')
    file.write(time_str + ':  ' + chat)
    file.flush()
    file.close()


def broadcast_messages():
    while True:
        if len(clients) > 0:
            broadcast_to_all = str(exchange_messages.get()).encode()
            for client in clients:
                client.send(broadcast_to_all)


thread_listen_to_clients = threading.Thread(target=listen_to_clients, args=(mySocket,))
thread_listen_to_clients.start()


thread_broadcast = threading.Thread(target=broadcast_messages)
thread_broadcast.start()


