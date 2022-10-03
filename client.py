
import socket
from threading import Thread
from tkinter import * #type: ignore
import random
from PIL import ImageTk, Image
import platform 
import tkinter as tk


screen_width = None
screen_height = None
SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None
canvas1 = None
canvas2 = None
nameEntry = None
nameWindow = None
gameWindow = None
ticket_grid = []
current_number_list = []
flash_number_list = []
flash_number_label = None

def game_window():
    global gameWindow
    global canvas2
    global screen_height
    global screen_width
    global dice
    global winning_message
    global reset_button
    global flash_number_label

    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry('800x600')
    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()
    bg = ImageTk.PhotoImage(file="assets/bg.jpeg")
    canvas2 = Canvas(gameWindow,width=500,height=500)
    canvas2.pack(fill="both",expand=True)
    canvas2.create_image(0,0,image=bg,anchor="nw")
    canvas2.create_text(float(screen_width)/4.5 ,50,text="Tambola Family Fun",
    font=("Chalkboard SE",50),fill="#3E2723")
    createTicket()
    placeNumbers()
    flash_number_label = canvas2.create_text(400,float(screen_height)/2.3,text="Waiting for other players to join",
    font=("Chalkboard SE",30),fill="#3E2723")
    gameWindow.resizable(True,True)
    gameWindow.mainloop()

def createTicket():
    global ticket_grid
    global gameWindow
    mainLabel = Label(gameWindow,width=65,height=16,relief='ridge',bd=5,bg="white")
    mainLabel.place(x=95,y=119)
    xPos = 105
    yPos = 130
    for row in range(0,3):
        row_list = []
        for coloumn in range(0,9):
            if platform.system() == "Darwin":
                box_button = Button(gameWindow,font=("Chalkboard SE",18),bd=3,
                padx=-22,pady=23,bg="#FFF176",
                highlightbackground="#FFF176",activebackground="#C5E1A5")
                box_button.place(x=xPos,y=yPos)
            else:
                box_button = tk.Button(gameWindow,font=("Chalkboard SE",30),width=3,
                height=2,borderwidth=5,bg="#FFF176")
                box_button.place(x=xPos,y=yPos)
            row_list.append(box_button)
            xPos +=64
        ticket_grid.append(row_list)
        yPos+=82
        xPos=105



def placeNumbers():
    global ticket_grid
    global current_number_list

    for row in range(0,3):
        random_col_list = []
        counter = 0
        while counter <=4:
            random_col=random.randint(0,8)
            if(random_col not in random_col_list):
                random_col_list.append(random_col)
                counter+=1

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()  # type: ignore
    nameEntry.delete(0,END) # type: ignore
    nameWindow.destroy()    # type: ignore

    SERVER.send(playerName.encode())  # type: ignore

    game_window()




def recieveMsg():
    pass

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1


    nameWindow = Tk()
    nameWindow.title("Tambola Family Fun")

    nameWindow.geometry('800x600')
    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()
    bg = ImageTk.PhotoImage(file="assets/bg.jpeg")
    canvas1 = Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill="both",expand=True)
    canvas1.create_image(0,0,image=bg,anchor='nw')
    canvas1.create_text(screen_width / 4.5, screen_height/8,text="Enter Name",font=("Chalkboard SE",60),
    fill="black")
    nameEntry = Entry(nameWindow,width=15,justify="center",font=("Chalkboard SE",30),bd=5,bg="white")
    nameEntry.place(x=screen_width/7,y=screen_height/5.5)
    button=Button(nameWindow,text="Save",font=("Chalkboard SE",30),width=11,command=saveName,height=2,
    bg="#80DEEA",bd=3)
    button.place(x=screen_width/6,y=screen_height/4)
    nameWindow.resizable(True,True)
    nameWindow.mainloop()



def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    PORT = 6000
    IP_ADDRESS = "127.0.0.1"
    

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    thread = Thread(target=recieveMsg)
    thread.start()
    askPlayerName()

setup()

