import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

SERVER_ADDR = '127.0.0.1'
PORT = 3000

# make TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDR, PORT))


class MyWeirdApp:

    def __init__(self, master):

        master.title('**Strange App**')
        master.configure(background='#4080bf')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#4080bf')
        self.style.configure('TButton', background='#4080bf')
        self.style.configure('TLabel', background='#4080bf', font=('Consolas', 10))

        self.frame_chat = ttk.Frame(master)
        self.frame_chat.pack(side=RIGHT)

        ttk.Label(self.frame_chat, text='Name:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_chat, text='Password:').grid(row=0, column=2, padx=5, sticky='sw')
        ttk.Label(self.frame_chat, text='Type message:').grid(row=4, column=1, columnspan=2, padx=5)
        self.name_holder = ttk.Label(self.frame_chat, text='**Welcome**')
        self.name_holder.grid(row=3, column=1, padx=5, sticky='sw')

        self.entry_name = ttk.Entry(self.frame_chat, width=24, font=('Consolas', 10))
        self.entry_psw = ttk.Entry(self.frame_chat, width=24, font=('Consolas', 10))
        self.text_message = Text(self.frame_chat, width=50, height=3, font=('Consolas', 10))
        self.text_chat_record = Listbox(self.frame_chat, height=30, width=50, font=('Consolas', 10))

        self.entry_name.grid(row=1, column=1, padx=5)
        self.entry_psw.grid(row=1, column=2, padx=5)
        self.text_message.grid(row=5, column=1, columnspan=2)
        self.text_chat_record.grid(row=7, column=1, columnspan=2, pady=5)

        self.new_user_btn = ttk.Button(self.frame_chat, text='new user', command=self.request_to_sign_up)
        self.new_user_btn.grid(row=3, column=2, padx=5, pady=5, sticky='w')

        self.log_in_btn = ttk.Button(self.frame_chat, text='log in', command=self.request_to_log_in)
        self.log_in_btn.grid(row=3, column=2, padx=5, pady=5, sticky='e')

        self.send_btn = ttk.Button(self.frame_chat, text='Send', command=self.collect_message)
        self.send_btn.grid(row=6, column=1, padx=5, pady=5, sticky='e')

        self.clear_btn = ttk.Button(self.frame_chat, text='Clear', command=self.clear)
        self.clear_btn.grid(row=6, column=2, padx=5, pady=5, sticky='w')

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
    def recv_messages(self, my_socket):
        chat_possible = False
        log_in_success = False
        while True:
            try:
                message_received = my_socket.recv(1024).decode()
            except ConnectionAbortedError:
                print('>>> Server has dropped connection')
                break
            except OSError:
                print('>>> Can not receive message from server')
                break
            else:
                if message_received.startswith('N_ER'):
                    error_msg = 'please choose another user name'
                    messagebox.showerror('error', error_msg)
                    self.clear()
                elif message_received.startswith('J_ER'):
                    error_msg = 'Can not find user, please try again'
                    messagebox.showerror('error', error_msg)
                    self.clear()
                elif message_received.startswith('J_OK'):
                    self.clear()
                    chat_possible = True
                    protocol, user_name = message_received.split(';')
                    print('J_OK')
                    self.list_online_users.insert(END, user_name)
                    log_info_text = 'you are log in as:\n' + user_name
                    self.name_holder.config(text=log_info_text)
                    self.entry_name.config(state=DISABLED)
                    self.entry_psw.config(state=DISABLED)
                    self.new_user_btn.config(state=DISABLED)
                    self.log_in_btn.config(state=DISABLED)
                elif message_received.startswith('DATA') and chat_possible is True:
                    self.text_chat_record.insert(END, message_received[5:])
                elif message_received.startswith('DATA') and chat_possible is False:
                    warning_msg = 'please log in or register first'
                    messagebox.showwarning('warning', warning_msg)

    def request_to_log_in(self):
        user_name = self.entry_name.get()
        user_psw = self.entry_psw.get()
        user = 'JOIN;' + user_name + ';' + user_psw
        client_socket.send(user.encode())

    def request_to_sign_up(self):
        user_name = self.entry_name.get()
        user_psw = self.entry_psw.get()
        user = 'JO_N;' + user_name + ';' + user_psw
        client_socket.send(user.encode())

    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_psw.delete(0, 'end')

    def collect_message(self):
        local_user_name = self.name_holder['text']
        user_message = self.text_message.get(1.0, 'end')
        user_message = 'DATA;' + local_user_name[19:] + ';' + user_message
        client_socket.send(user_message.encode())
        self.text_message.delete(1.0, 'end')


def main():
    root = Tk()
    app = MyWeirdApp(root)
    recv_message_thread = threading.Thread(target=app.recv_messages, args=(client_socket,))
    recv_message_thread.start()
    root.mainloop()


if __name__ == '__main__':
    main()

