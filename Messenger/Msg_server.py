import socket
import queue
import threading

clients = []

host = "127.0.0.1"
port = 3000
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind((host, port))
mySocket.listen(5)

def listenToClients(socket):
    while True:
        conn, addr = socket.accept()
        clients.append(conn)


