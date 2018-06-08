import socket
import threading
from tkinter import *

SERVER_ADDR = '127.0.0.1'
PORT = 3000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDR, PORT))


root = Tk()

left_frame = Frame(root)
left_frame.pack(side=LEFT)

right_frame = Frame(root)
right_frame.pack()

# top_frame = Frame(right_frame)
# top_frame.pack()

label = Label(left_frame, text="placeholder")
label.pack()

text_input = Text(right_frame, height=2, width=42)
text_input.pack(side=TOP)

message = ""

# set TCP/IP socket

# while message != 'EXIT':
#     message = input(':')
#     client_socket.send(message.encode())

# client_socket.close()

# --------------function--------------------------------


def display_message():
    message = text_input.get(1.0, END)
    client_socket.send(message.encode())
    print(message.strip())


def recv_messages(my_socket):
    while True:
        try:
            message_received = my_socket.recv(1024).decode()
        except ConnectionAbortedError:
            print('>>> Can not receive message from server')
            break
        except OSError:
            print('>>> Can not receive message from server')
            break
        else:
            text_chat.insert(END, message_received)
            print('>>> ' + message_received)


send_thread = threading.Thread(target=recv_messages, args=(client_socket,))
send_thread.start()

thread_total = threading.active_count()
print('{:d} threads are running on the client side'.format(thread_total))

# ------------------------------------------------------
# command=lambda: recv_messages(client_socket)


send_button = Button(right_frame, text="send", command=display_message)
send_button.pack(side=TOP)


# bottom_frame = Frame(right_frame)
# bottom_frame.pack()

text_chat = Text(right_frame, height=30, width=50)
text_chat.pack(side=BOTTOM)
text_chat.insert(END, "to demonstrate chat history, should be view only")

root.mainloop()


#
# if __name__ == '__main__':
#     main()


