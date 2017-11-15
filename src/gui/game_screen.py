import Tkinter
import platform
import tkFileDialog as filedialog
from Tkinter import *

from oosudoku import *

if platform.system() == 'Windows':
    small_font = ("Courier New", "10", "bold")
    large_font = ("Courier New", "21", "bold")
else:
    small_font = ("Courier New", "10", "bold")
    large_font = ("Courier New", "25", "bold") 


box_size = 50
half = box_size/2

class NumberButtons(Frame):
    """ A frame containing the 9 choice buttons """

    def __init__(self, parent):
        Frame.__init__(self, parent, relief=SUNKEN, bg = "grey")
        self.buttons = []
        self.current = IntVar()
        for i in range(1,10):
            bi = Radiobutton(self, text = str(i), value = i, 
                             variable = self.current,
                             indicatoron=0,
                             font = large_font, fg = "red",
                             selectcolor="yellow")
            bi.pack(ipadx = 4,pady = 6)
            self.buttons.append(bi)
        self.current.set(1)


    def get_current(self):
        """ Return the current choice """

        return self.current.get()


                    ############################
                    #===== COMMANDS CLASS =====#
                    ############################

class Commands(Frame):
    """ Create :
        3 Buttons which interact with the canvas
        Button 1 : Show or Hide the available choices for the game
        Button 2 : Auto fill or not the game
        Button 3 : Undo the latest action
    """
    def __init__(self, parent, canvas):
        Frame.__init__(self, parent, bg = "grey")

        self.canvas = canvas
        self.sudoku = None

    #=== Three Buttons ====#


    #=== Create Buttons Events ====#


    def SetSudoku(self, sudoku):
        self.sudoku = sudoku


                    ########################
                    #===== VIEW CLASS =====#
                    ########################

class View(Frame):
    """ Create:
        1 canvas with 9x9 Texts (i.e. sudoku case) + Ligns
        1 Table which contains ids of all Text items logically related to the table sudoku.game[][]
        1 Label wich displays the state of the game
    """
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "grey")

        self.sudoku = None
        self.numberbuttons = None
        self.commands = None

        #=== Canvas ===#

        # Initialize the Canvas
        self.CanvasSize = 500 
        self.CanvasGame = Canvas(self, width = self.CanvasSize-2, height = self.CanvasSize-2, bg = "white", relief = "solid", bd = 4)
        self.CanvasGame.pack(padx = 20, pady = 20)
        self.table = []

        # Create Canvas Items (Ligns + 9x9 Texts)  + 1 Label
        for i in range(1,10):
            if (i == 3) or (i == 6): width = 4
            else: width = 1
            self.CanvasGame.create_line(4+i*self.CanvasSize/9, 0, 4+i*self.CanvasSize/9, self.CanvasSize+10, width = width, state="disabled")
            self.CanvasGame.create_line(0, 4+i*self.CanvasSize/9, self.CanvasSize+10, 4+i*self.CanvasSize/9, width = width, state="disabled")
            itemsid = []
            for j in range(1,10):
                itemsid.append(self.CanvasGame.create_text(4+(2*i-1)*self.CanvasSize/18, 4+(2*j-1)*self.CanvasSize/18, anchor = CENTER, tag='Text', text = " ", font = large_font, fill="red"))
            self.table.append(itemsid)

        self.labelVariable = StringVar()
        self.labelVariable.set("")
        self.label = Label(self, textvariable=self.labelVariable, font = large_font, bg="grey", fg="red")
        self.label.pack(pady = 10)

        #==== Create Mouse Event ===#
        """If the Player click on a empty "case" (i.e. item with a tag 'Text') and the number he tries to insert is consistent with the
        available choices, he will success. Otherwise nothing happens. After each success, the display is updated"""

        self.CanvasGame.bind("<Button-1>", self.Write) # If the player left-click on the canvas => execute the method Write

    def Write(self, event):
        if self.sudoku != None: # To be sure that the user cannot interact with the canvas when no game is loaded
            items = self.CanvasGame.find_enclosed(event.x - 35,event.y -35 , event.x +35,event.y +35) # We consider all items enclosed in a square 70x70 where the user clicked (the size of the square depends strongly on the canvas.size) 
            item = list_intersection(items, self.CanvasGame.find_withtag('Text')) # We just consider previous selected items which are empty "case"(i.e. item with a tag 'Text')
            if len(item) == 1:
                for i in range(0,9):
                    for j in range(0,9):
                        if int(item[0]) == int(self.table[j][i]):
                            if str(self.numberbuttons.get_current()) in self.sudoku.choices(i,j): # We check what the user tries to insert is consistent with the available choices
                                self.sudoku.set_entry(i,j,str(self.numberbuttons.get_current()))  # We Update game[][]
                                for t in self.sudoku._undo_stack[-1]:
                                    self.CanvasGame.itemconfig(self.table[t[1]][t[0]], tag='Fixed')
                                self.Update() # We update the display
       
        #==== Update Items ===#

    def Update(self):
        # Update the Label
        self.labelVariable.set(self.sudoku.game_status())
        # Update the Fixed Numbers --> All items which are "Fixed" tagged are displayed in red
        for i in range(0,9):
            for j in range(0,9):
                if " " not in self.sudoku._game[i][j]:
                    self.CanvasGame.itemconfig(self.table[j][i], text=self.sudoku._game[i][j], font = large_font, tag='Fixed', fill="red")
        # Update the choices Numbers --> All items which are "Text" tagged are displayed in blue or not (depending on the Show/Hide choices Button)



        #==== GET/SET Methods ===#
        
    def SetNumberButtons(self, numberbuttons):
        self.numberbuttons = numberbuttons
    def SetSudoku(self, sudoku):
        self.sudoku = sudoku
    def SetCommands(self, commands):
        self.commands = commands


                    ##############################
                    #===== CONTROLLER CLASS =====#
                    ##############################



class Controller(Frame):
    """ Create:
        2 Frames : one contains a view instance(canvas + lable), the other contains a numberbuttons instance and a commands instance
        1 menu "File" which give the possibility:
            * to open a file and load a game
            * Exit the game
    """
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "grey")
        self.parent = parent
        self.F1 = Frame(parent, bd=5, bg = "grey", relief="sunken")
        self.F2 = Frame(parent, bg="grey")
        self.view = View(self.F1)
        self.numberbuttons = NumberButtons(self.F2)
        self.view.SetNumberButtons(self.numberbuttons)
        self.commands = Commands(self.F2, self.view)

        #MenuBar
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Begin Game", command=self.LoadGame)
        self.filemenu.add_command(label="Exit", command=self.QuitGame)
        self.menubar.add_cascade(label="Begin or Exit", menu=self.filemenu)
        parent.config(menu=self.menubar)

        #Display
        self.F1.pack(fill = Y, side=LEFT)
        self.F2.pack(fill = Y, side=LEFT)
        self.view.pack(side = LEFT, padx = 30)
        self.numberbuttons.pack(side = LEFT, padx = 20)
        self.commands.pack(side = LEFT)






        #=== Function LoadGame & QuitGame ===#

    def LoadGame(self):
        
        # Open a file
        filePath = 'game.txt' # The user has to open a file

        # Initialization : We check if it is a proper sudoku game file. Otherwise we print a message on the stdout
        #try:
        self.sudoku = Sudoku(filePath, False)
        self.commands.SetSudoku(self.sudoku)
      #  self.commands.Button1.config(state = "normal") # The 3 Buttons become usable when the user loads a proper game
     #   self.commands.Button2.config(state = "normal")
      #  self.commands.Button3.config(state = "normal")
        self.view.SetSudoku(self.sudoku)
        self.view.SetCommands(self.commands)
        self.view.Update()

        # except Exception as e:
        #     print("This is not a proper sudoku game file - Try again !")
        #     print(e)

    def QuitGame(self): # if the user press exit in the menu => we close the window and stop the program
        self.parent.destroy()
        self.parent.quit()

##

class SudokuApp():
    """ The Sudoku application """

    def __init__(self, master=None):
        master.title("Sudoku")
        master.config(bg = "grey")
        master.resizable(0,0)
        self.controller = Controller(master)




