import socket
import threading
from tkinter import *
from tkinter import ttk

SERVER_ADDR = '127.0.0.1'
PORT = 3000

# make TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDR, PORT))


class MyWeirdApp:

    def __init__(self, master):

        master.title("**Strange App**")
        master.resizable(False, False)
        master.configure(background='#4080bf')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#4080bf')
        self.style.configure('TButton', background = '#4080bf')
        self.style.configure('TLabel', background = '#4080bf', font = ('Consolas', 10))

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text='Name:').grid(row=0, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Password:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Type message:').grid(row=4, column=0, padx=5, sticky='sw')

        self.entry_name = ttk.Entry(self.frame_content, width=24, font=('Consolas', 10))
        self.entry_psw = ttk.Entry(self.frame_content, width=24, font=('Consolas', 10))
        self.text_message = Text(self.frame_content, width=50, height=3, font=('Consolas', 10))
        self.text_chat_record = Listbox(self.frame_content, height=30, width=50, font=('Consolas', 10))

        self.entry_name.grid(row=1, column=0, padx=5)
        self.entry_psw.grid(row=1, column=1, padx=5)
        self.text_message.grid(row=4, column=0, columnspan=2)
        self.text_chat_record.grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Button(self.frame_content, text='connect')\
            .grid(row=3, column=1, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Send', command=self.collect_message)\
            .grid(row=5, column=0, padx=5, pady=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear')\
            .grid(row=5, column=1, padx=5, pady=5, sticky='w')

    def collect_message(self):
        user_message = self.text_message.get(1.0, 'end')
        client_socket.send(user_message.encode())

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
                self.text_chat_record.insert(END, message_received)
                print(message_received)

def main():
    root = Tk()
    app = MyWeirdApp(root)
    recv_message_thread = threading.Thread(target=app.recv_messages, args=(client_socket,))
    recv_message_thread.start()
    root.mainloop()


if __name__ == '__main__':
    main()

