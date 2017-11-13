from Tkinter import *

from src.gui.client import get_nickname, get_address
import tkMessageBox
import Tkinter as tk

def get_nick_text():
    nick_name = nick_text.get("1.0",'end-1c')
    if get_nickname(nick_name) == 1:
        write_names = open("nicknames", "a")
        #read_names = open("nickname","a")
        write_names.write("\n"+nick_name)
        connect_to_server()
    else:
        error_message("your nickname is not valid")

def error_message(message):
    tkMessageBox.showerror("Title", message)

def info_message(message):
    tkMessageBox.showinfo("Title", message)

def on_select(event):
    print event.widget.curselection()[0]

def create_login_screen():
    read_names = open("nicknames", "r")
    names = read_names.read().split()
    global login
    login = Tk()
    login.title("Enter Nickname")
    global list_name
    list_name = Listbox(login, selectmode='single')
    list_name.bind('<<ListboxSelect>>', on_select)
    i = 0
    for n in names:
        list_name.insert(i,n)
        i+=1
    list_name.pack()
    okay = Button(login, text="ok", command=get_nick_text, width=20)
    okay.pack({"side": "bottom"})
    nick_label = Label(login, text="Your Nickname")
    nick_label.pack()
    global nick_text
    nick_text = Text(login, width=50, height=2)
    nick_text.pack()
    mainloop()

def connect_to_server():
    login.destroy()
    root = Tk()
    root.title("Enter Sudoku server address")
    okay = Button(root, text="ok", command=get_address_port, width=20)
    okay.pack({"side": "bottom"})
    address_label = Label(root, text="server address")
    address_label.pack()
    global address_text
    address_text = Text(root, width=50, height=2)
    address_text.pack()
    port_label = Label(root, text="port")
    port_label.pack()
    global port_text
    port_text = Text(root, width=50, height=2)
    port_text.pack()
    mainloop()

def get_address_port():
    address_server = address_text.get("1.0",'end-1c')
    port = port_text.get("1.0",'end-1c')
    get_address(address_server,port)

def multiplayer_game():
    game = Tk()
    game.title("Multiplayer Game Dialog ")
    list_sessions = Listbox(game,height = 5)
    i = 0
    sessions = ["fghj","efdsf","fsd"]
    for n in sessions:
        list_sessions.insert(i, n)
        i += 1
    list_sessions.pack()
    okay = Button(game, text="create new session", command = create_session, width=20)
    okay.pack({"side": "bottom"})
    mainloop()

def create_session():
    global session
    session = Tk()
    session.title("Creating new Sudoku Solving Session")
    okay = Button(session, text="ok", command=game_player, width=20)
    okay.pack({"side": "bottom"})
    num_label = Label(session, text="Player's number:")
    num_label.pack()
    global player_num_text
    player_num_text = Text(session, width=50, height=2)
    player_num_text.pack()
    mainloop()

def game_player():
    print "game"

create_login_screen()

#multiplayer_game()

#create_session()





