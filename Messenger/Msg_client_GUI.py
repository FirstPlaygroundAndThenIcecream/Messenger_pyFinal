import socket
import threading
from tkinter import *
from tkinter import ttk
import msg_db

SERVER_ADDR = '127.0.0.1'
PORT = 3000

# make TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDR, PORT))


class MyWeirdApp:

    def __init__(self, master):

        master.title("**Strange App**")
        master.configure(background='#4080bf')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#4080bf')
        self.style.configure('TButton', background = '#4080bf')
        self.style.configure('TLabel', background = '#4080bf', font = ('Consolas', 10))

        self.frame_chat = ttk.Frame(master)
        self.frame_chat.pack(side=RIGHT)

        ttk.Label(self.frame_chat, text='Name:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_chat, text='Password:').grid(row=0, column=2, padx=5, sticky='sw')
        ttk.Label(self.frame_chat, text='Type message:').grid(row=3, column=1, padx=5, sticky='sw')

        self.entry_name = ttk.Entry(self.frame_chat, width=24, font=('Consolas', 10))
        self.entry_psw = ttk.Entry(self.frame_chat, width=24, font=('Consolas', 10))
        self.text_message = Text(self.frame_chat, width=50, height=3, font=('Consolas', 10))
        self.text_chat_record = Listbox(self.frame_chat, height=30, width=50, font=('Consolas', 10))

        self.entry_name.grid(row=1, column=1, padx=5)
        self.entry_psw.grid(row=1, column=2, padx=5)
        self.text_message.grid(row=4, column=1, columnspan=2)
        self.text_chat_record.grid(row=6, column=1, columnspan=2, pady=5)

        ttk.Button(self.frame_chat, text='connect', command=self.request_to_connect)\
            .grid(row=3, column=2, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_chat, text='Send', command=self.collect_message)\
            .grid(row=5, column=1, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_chat, text='Clear', command=self.clear)\
            .grid(row=5, column=2, padx=5, pady=5, sticky='w')

        self.frame_multipurpose = ttk.Frame(master)
        self.frame_multipurpose.pack(side=LEFT)

        ttk.Label(self.frame_multipurpose, text='Online users').grid(row=0, column=0, pady=5)
        self.list_online_users = Listbox(self.frame_multipurpose, height=30, width=20, font=('Consolas', 10))
        self.list_online_users.grid(row=1, column=0)

        ttk.Button(self.frame_multipurpose, text='delete') \
            .grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.frame_multipurpose, text='brute force') \
            .grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.frame_multipurpose, text='whatever') \
            .grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.frame_multipurpose, text='another') \
            .grid(row=5, column=0, padx=5, pady=5)

# -----------------------------event--------------------------------------------------------------------------
    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_psw.delete(0, 'end')
        # self.text_message.delete(1.0, 'end')

    def collect_message(self):
        user_message = self.text_message.get(1.0, 'end')
        client_socket.send(user_message.encode())
        self.text_message.delete(1.0, 'end')

    def recv_messages(self, my_socket):
        while True:
            try:
                message_received = my_socket.recv(1024).decode()
                print(type(message_received))
            except ConnectionAbortedError:
                print('>>> Can not receive message from server')
                break
            except OSError:
                print('>>> Can not receive message from server')
                break
            else:
                # if not message_received:
                #     break
                # else:
                if message_received.startswith('J_OK'):
                    print('J_OK')
                    self.list_online_users.insert(END, self.entry_name.get())
                    self.clear()
                elif message_received.startswith('DATA'):
                    self.text_chat_record.insert(END, message_received)
                    print(message_received)

    def request_to_connect(self):
        # verify user
        # user exist -> messagebox
        # rename
        # send and add
        user_name = self.entry_name.get()
        user_psw = self.entry_psw.get()
        user = 'JOIN;' + user_name + ';' + user_psw
        client_socket.send(user.encode())



def main():
    root = Tk()
    app = MyWeirdApp(root)
    recv_message_thread = threading.Thread(target=app.recv_messages, args=(client_socket,))
    recv_message_thread.start()
    root.mainloop()


if __name__ == '__main__':
    main()

