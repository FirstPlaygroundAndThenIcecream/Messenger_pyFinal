import socket
import threading
from tkinter import *

SERVER_ADDR = '127.0.0.1'
PORT = 3000

root = Tk()

top_frame = Frame(root)
top_frame.pack()

text_input = Text(top_frame, height=2, width=42)
text_input.pack(side=LEFT)
text_input.insert(END, "user type message here\n")

# --------------function--------------------------------


def display_message():
    content = text_input.get(1.0, END)
    print(content.strip())
    text_chat.insert(END, content)

# ------------------------------------------------------


send_button = Button(top_frame, text="send", command=display_message)
send_button.pack()


bottom_frame = Frame(root)
bottom_frame.pack()

text_chat = Text(bottom_frame, height=30, width=50)
text_chat.pack(side=BOTTOM)
text_chat.insert(END, "to demonstrate chat history, should be view only")


root.mainloop()

def main():
    message = ""

    # set TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDR, PORT))


    send_thread = threading.Thread(target=recv_messages, args=(client_socket,))
    send_thread.start()

    thread_total = threading.active_count()
    print('{:d} threads are running on the client side'.format(thread_total))

    while message != 'EXIT':
        message = input(':')
        client_socket.send(message.encode())

    client_socket.close()


def recv_messages(my_socket):
    while True:
        try:
            message_received = my_socket.recv(1024).decode()
            print('>>> ' + message_received)
        except ConnectionAbortedError:
            print('>>> Can not receive message from server')
            break
        except OSError:
            print('>>> Can not receive message from server')
            break


if __name__ == '__main__':
    main()


