import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from itertools import product
import string
from time import gmtime, strftime

SERVER_ADDR = '127.0.0.1'
PORT = 3000

# make TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDR, PORT))


class MyWeirdApp:

    def __init__(self, master):
        bg_color = '#004466'
        text_color = '#94b8b8'

        master.title('**Strange App**')
        master.configure(background=bg_color)

        self.style = ttk.Style()
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TButton', background=bg_color, foreground='#004466')
        self.style.configure('TLabel', background=bg_color, font=('Consolas', 10), foreground=text_color)

        self.frame_chat = ttk.Frame(master)
        self.frame_chat.pack(side=RIGHT)

        ttk.Label(self.frame_chat, text='Name:').grid(row=0, column=1, padx=5, pady=2, sticky='sw')
        ttk.Label(self.frame_chat, text='Password:').grid(row=0, column=2, padx=5, pady=2, sticky='sw')
        ttk.Label(self.frame_chat, text='Type message:').grid(row=5, column=1, columnspan=2, padx=5)
        self.name_holder = ttk.Label(self.frame_chat, text='**Welcome**')
        self.name_holder.grid(row=4, column=1, columnspan=2, padx=5, sticky='sw')

        self.entry_name = ttk.Entry(self.frame_chat, width=24, font=('Consolas', 10))
        self.entry_psw = ttk.Entry(self.frame_chat, show='*', width=24, font=('Consolas', 10))
        self.text_message = Text(self.frame_chat, width=50, height=3, font=('Consolas', 10))
        self.text_chat_record = Listbox(self.frame_chat, height=30, width=50, font=('Consolas', 10))

        self.entry_name.grid(row=1, column=1, padx=5)
        self.entry_psw.grid(row=1, column=2, padx=5)
        self.text_message.grid(row=6, column=1, columnspan=2)
        self.text_chat_record.grid(row=8, column=1, columnspan=2, pady=7)

        self.new_user_btn = ttk.Button(self.frame_chat, text='new user', command=self.request_to_sign_up)
        self.new_user_btn.grid(row=3, column=1, padx=5, pady=5, sticky='e')

        self.log_in_btn = ttk.Button(self.frame_chat, text='log in', command=self.request_to_log_in)
        self.log_in_btn.grid(row=3, column=2, padx=5, pady=5, sticky='w')

        self.log_out_btn = ttk.Button(self.frame_chat, text='log out', command=self.request_to_log_out)
        self.log_out_btn.grid(row=3, column=2, padx=5, pady=5, sticky='e')

        self.send_btn = ttk.Button(self.frame_chat, text='Send', command=self.collect_message)
        self.send_btn.grid(row=7, column=1, padx=5, pady=5, sticky='e')

        self.clear_btn = ttk.Button(self.frame_chat, text='Clear', command=self.clear)
        self.clear_btn.grid(row=7, column=2, padx=5, pady=5, sticky='w')

        self.frame_multipurpose = ttk.Frame(master)
        self.frame_multipurpose.pack(side=LEFT)

        ttk.Label(self.frame_multipurpose, text='Online users').grid(row=0, column=0, pady=5)
        self.list_online_users = Listbox(self.frame_multipurpose, height=31, width=20, font=('Consolas', 10))
        self.list_online_users.grid(row=1, column=0, padx=5)
        self.force_info = ttk.Label(self.frame_multipurpose, text='')
        self.force_info.grid(row=2, column=0, padx=5, pady=5)

        self.delete_chat_btn = ttk.Button(self.frame_multipurpose, text='delete chat', command=self.delete_all_chat_record)
        self.delete_chat_btn.grid(row=3, column=0, pady=5)
        self.brute_force_btn = ttk.Button(self.frame_multipurpose, text='brute force', command=self.test_brute_force)
        self.brute_force_btn.grid(row=4, column=0, padx=5, pady=5)
        self.bg_color_btn_o = ttk.Button(self.frame_multipurpose, text='Ocean', command=self.change_bg_color_ocean)
        self.bg_color_btn_o.grid(row=5, column=0, padx=5, pady=5)
        self.bg_color_btn_d = ttk.Button(self.frame_multipurpose, text='Desert', command=self.change_bg_color_desert)
        self.bg_color_btn_d.grid(row=6, column=0, padx=5, pady=5)


# -----------------------------receive message thread------------------------------------------------------------------

    def recv_messages(self, my_socket):
        self.disable_service()
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
                    self.disable_service()
                elif message_received.startswith('J_ER'):
                    error_msg = 'Can not find user, please try again'
                    messagebox.showerror('error', error_msg)
                    self.disable_service()
                elif message_received.startswith('J_OK'):
                    self.clear()
                    protocol, user_name = message_received.split(';')
                    print('J_OK' + ' ' + user_name)
                    # self.list_online_users.insert(END, user_name)
                    log_info_text = 'you are log in as: ' + user_name
                    time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    self.name_holder.config(text=log_info_text)
                    self.disable_log_in()
                    self.enable_service()
                    self.text_chat_record.insert(END, time_str)

                elif message_received.startswith('DATA'):
                    print(message_received)
                    self.enable_service()
                    self.disable_log_in()
                    self.text_chat_record.insert(END, message_received[5:])

                elif message_received.startswith('LIST'):
                    online_users = message_received.split(';')[1]
                    online_users_list = online_users.split(' ')
                    self.list_online_users.delete(0, END)
                    for user in online_users_list:
                        self.list_online_users.insert(END, user)

                elif message_received.startswith('REMV'):
                    print(message_received)
                    log_out_msg = 'you have log out, please log in to use our service again'
                    messagebox.showinfo('info', log_out_msg)
                    self.disable_service()
                    self.enable_log_in()

# --------------------------events---------------------------------------------------------

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

    def request_to_log_out(self):
        user_name = self.get_user_name()
        user_message = 'QUIT' + ';' + user_name
        client_socket.send(user_message.encode())

    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_psw.delete(0, 'end')

    def collect_message(self):
        local_user_name = self.get_user_name()
        user_message = self.text_message.get(1.0, 'end')
        user_message = 'DATA;' + local_user_name + ';' + user_message
        client_socket.send(user_message.encode())
        self.text_message.delete(1.0, 'end')

    def get_user_name(self):
        return self.name_holder['text'][19:]

    def disable_chat_input(self):
        self.text_message.config(state=DISABLED)
        self.send_btn.config(state=DISABLED)
        self.clear_btn.config(state=DISABLED)

    def enable_chat_input(self):
        self.text_message.config(state=NORMAL)
        self.send_btn.config(state=NORMAL)
        self.clear_btn.config(state=NORMAL)

    def disable_log_in(self):
        self.entry_name.config(state=DISABLED)
        self.entry_psw.config(state=DISABLED)
        self.new_user_btn.config(state=DISABLED)
        self.log_in_btn.config(state=DISABLED)

    def enable_log_in(self):
        self.name_holder.config(text='**Welcome**')
        self.entry_name.config(state=NORMAL)
        self.entry_psw.config(state=NORMAL)
        self.new_user_btn.config(state=NORMAL)
        self.log_in_btn.config(state=NORMAL)

    def disable_user_list_chat_record(self):
        self.list_online_users.config(state=DISABLED)
        self.text_chat_record.config(state=DISABLED)

    def enable_user_list_chat_record(self):
        self.list_online_users.config(state=NORMAL)
        self.text_chat_record.config(state=NORMAL)

    def test_brute_force(self):
        digits = string.digits
        combination = [''.join(i) for i in product(digits, repeat=4)]
        for each in combination:
            if each == '8989':
                self.force_info.config(text=each)

    def delete_all_chat_record(self):
        self.text_chat_record.delete(0, END)

    def disable_btn_group(self):
        self.delete_chat_btn.config(state=DISABLED)
        self.brute_force_btn.config(state=DISABLED)
        self.bg_color_btn_o.config(state=DISABLED)
        self.bg_color_btn_d.config(state=DISABLED)

    def enable_btn_group(self):
        self.delete_chat_btn.config(state=NORMAL)
        self.brute_force_btn.config(state=NORMAL)
        self.bg_color_btn_o.config(state=NORMAL)
        self.bg_color_btn_d.config(state=NORMAL)

    def disable_service(self):
        self.disable_chat_input()
        self.disable_btn_group()
        self.disable_user_list_chat_record()

    def enable_service(self):
        self.enable_chat_input()
        self.enable_user_list_chat_record()
        self.enable_btn_group()

    def change_bg_color_desert(self):
        bg_color = '#cc6600'
        text_color = '#391d13'
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TButton', background=bg_color, foreground=text_color)
        self.style.configure('TLabel', background=bg_color, foreground=text_color)

    def change_bg_color_ocean(self):
        color = '#4080bf'
        self.style.configure('TFrame', background=color)
        self.style.configure('TButton', background=color)
        self.style.configure('TLabel', background=color)


def main():
    root = Tk()
    app = MyWeirdApp(root)
    recv_message_thread = threading.Thread(target=app.recv_messages, args=(client_socket,))
    recv_message_thread.start()
    root.mainloop()


if __name__ == '__main__':
    main()

