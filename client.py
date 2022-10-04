

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
game_over = False
marked_number_list = []
displayed_number_list = []
dice = None
winning_message = None
reset_button = None


def showWrongMarking():
    global ticket_grid
    global flash_number_list

    # changing background color of number which is not flash yet on screen
    for row in ticket_grid:
        for numberBox in row:
            if(numberBox['text']):
                if(int(numberBox['text']) not in flash_number_list):
                    if(platform.system() == 'Darwin'):
                        # For Mac Users
                        numberBox.configure(state='disabled', disabledbackground='#f48fb1',
                            disabledforeground="white")
                    else:
                        # For Windows Users
                        numberBox.configure(state='disabled', background='#f48fb1',
                            foreground="white")

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

def markNumber(button):
    global marked_number_list
    global flash_number_list
    global playerName
    global SERVER
    global current_number_list
    global game_over
    global flash_number_label
    global canvas2

    buttonText = int(button['text'])
    marked_number_list.append(buttonText)

    # Make button disabled and changing color to green
    if(platform.system() == 'Darwin'):
        # For Mac Users
        button.configure(state='disabled',disabledbackground='#c5e1a5', disabledforeground="black", highlightbackground="#c5e1a5")
    else:
        # For Windows Users
        button.configure(state='disabled',background='#c5e1a5', foreground="black")

    winner =  all(item in flash_number_list for item in marked_number_list)

    if(winner and sorted(current_number_list) == sorted(marked_number_list)):
        message = playerName + ' wins the game.'  # type: ignore
        SERVER.send(message.encode())  # type: ignore
        return

    # When user lose the game
    if(len(current_number_list) == len(marked_number_list)):
        winner =  all(item in flash_number_list for item in marked_number_list)
        if(not winner):
            gameOver = True
            message = 'You Lose the Game'
            canvas2.itemconfigure(flash_number_label, text = message, font = ('Chalkboard SE', 40))  # type: ignore
            showWrongMarking()

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
                box_button.configure(command = lambda box_button=box_button : markNumber(box_button))

                box_button.place(x=xPos,y=yPos)
            else:
                box_button = tk.Button(gameWindow,font=("Chalkboard SE",30),width=3,
                height=2,borderwidth=5,bg="#FFF176")
                box_button.configure(command = lambda box_button=box_button : markNumber(box_button))
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
        numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50 , 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
        }


        counter = 0
        while (counter < len(random_col_list)):
            colNum = random_col_list[counter]
            numbersListByIndex = numberContainer[str(colNum)]
            randomNumber = random.choice(numbersListByIndex)

            if(randomNumber not in current_number_list):
                numberBox = ticket_grid[row][colNum]
                numberBox.configure(text=randomNumber, fg="black")
                current_number_list.append(randomNumber)

                counter+=1

    for row in ticket_grid:
        for numberBox in row:
            if not numberBox['text']:
                numberBox.configure(state='disabled', background="#ff8a65")

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
    global SERVER
    global displayed_number_list 
    global flash_number_label
    global canvas2
    global game_over
    
    numbers = [str(i)for i in range(1,91)]
    while True:
        chunk = SERVER.recv(2048).decode() # type: ignore
        if chunk in numbers and flash_number_label and not game_over:
            flash_number_list.append(int(chunk))
            canvas2.itemconfigure(flash_number_label,text=chunk,font=("Chalkboard SE",60))  # type: ignore
        elif 'wins the game.' in chunk:
            game_over = True
            canvas2.itemconfigure(flash_number_label,text=chunk,font=("Chalkboard SE",40))  # type: ignore




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

