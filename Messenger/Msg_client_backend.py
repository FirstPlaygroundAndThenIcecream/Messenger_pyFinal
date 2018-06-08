import socket
import threading

SERVER_ADDR = '127.0.0.1'
PORT = 3000


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDR, PORT))

    while True:

