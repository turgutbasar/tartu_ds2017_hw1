from Tkinter import *

from client import get_nickname, send_session_id, create_game_session, get_address
import tkMessageBox
from game_screen import SudokuApp

name = ''

def get_nick_text():
    global nick_name
    nick_name = nick_text.get("1.0",'end-1c')
    if get_nickname(nick_name) == 1:
        write_names = open("nicknames", "a")
        write_names.write("\n"+nick_name)
        connect_to_server()
    else:
        error_message("your nickname is not valid")

def error_message(message):
    tkMessageBox.showerror("Title", message)

def info_message(message):
    tkMessageBox.showinfo("Title", message)

def on_select(event):
    #print event.widget.curselection()[0]
    print list_name.get(list_name.curselection())
    global name
    name = list_name.get(list_name.curselection())
    connect_to_server()

def create_game_screen():
    sudoku = Tk()
    app = SudokuApp(sudoku)
    mainloop()

# show nickname screen
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
    nick_text = Text(login, width=50, height=5)
    nick_text.pack()
    mainloop()
# connect to server screen
def connect_to_server():
    login.destroy()
    global root
    root = Tk()
    root.title("Enter Sudoku server address")
    okay = Button(root, text="ok", command=get_address_port, width=20)
    okay.pack({"side": "bottom"})
    address_label = Label(root, text="server address",font=("Arial", 10))
    address_label.pack()
    global address_text
    address_text = Text(root, width=50, height=2, font=("Arial", 10))
    address_text.pack()
    port_label = Label(root, text="port",font=("Arial", 10))
    port_label.pack()
    global port_text
    port_text = Text(root, width=50, height=2,font=("Arial", 10))
    port_text.pack()
    mainloop()

def get_address_port():
    address_server = address_text.get("1.0", 'end-1c')
    port = port_text.get("1.0", 'end-1c')
    if name == '':
        print "nickname",nick_name
        get_address(address_server,port,nick_name, notify_callback)
    else:
        print "name", name
        get_address(address_server,port,name, notify_callback)


def notify_callback( type, data):
    print("data:" + str(type))
    if type == 0:
        multiplayer_game(data)
    else:
        create_session()
    return

def on_click_sessions(event):
    current_session = list_box_sessions.get(list_box_sessions.curselection())
    print current_session
    send_session_id(current_session)

def multiplayer_game(list_sessions):
    root.destroy()
    global game
    game = Tk()
    game.title("Multiplayer Game Dialog ")
    global list_box_sessions
    list_box_sessions = Listbox(game,height = 5,font=("Arial", 10),selectmode='single')
    list_box_sessions.bind('<<ListboxSelect>>', on_click_sessions)
    i = 0
    for n in list_sessions:
        list_box_sessions.insert(i, n)
        i += 1
    list_box_sessions.pack()
    okay = Button(game, text="create new session", command = create_session, width=20)
    okay.pack({"side": "bottom"})
    mainloop()

def create_session():
    print("create sesson")
    game.destroy()
    global session
    session = Tk()
    session.title("Creating new Sudoku Solving Session")
    okay = Button(session, text="ok", command = create_new_session, width=20)
    okay.pack({"side": "bottom"})
    num_label = Label(session, text="Player's number:")
    num_label.pack()
    global player_num_text
    player_num_text = Text(session, width=50, height=2)
    player_num_text.pack()
    mainloop()

def create_new_session():
    player_num = player_num_text.get("1.0", 'end-1c')
    create_game_session(player_num)
    print "game"

def game_player_scenario():
    print "senario"

create_login_screen()

#multiplayer_game(9)

#create_session()





