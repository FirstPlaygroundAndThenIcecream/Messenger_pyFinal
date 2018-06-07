import socket
import threading

SERVER_ADDR = '127.0.0.1'
PORT = 3000


def main():
    message = ""

    # set TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDR, PORT))

    send_thread = threading.Thread(target=recv_messages, args=(client_socket,))
    send_thread.start()

    while message != 'EXIT':
        message = input(':')
        client_socket.send(message.encode())

    client_socket.close()


def recv_messages(my_socket):
    while True:
        message_received = my_socket.recv(1024).decode()
        print('>>> ' + message_received)


if __name__ == '__main__':
    main()


