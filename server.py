import socket
from threading import Thread
import time
import random

SERVER = None
IP_ADDRESS = "127.0.0.1"
PORT = 6000

CLIENTS = {}

FLASH_NUMBER_LIST=[i for i in range(1,91)]
players_joined = False

def recvMsg(player_socket):
    global CLIENTS
    global gameOver

    while True:
        try:
            message = player_socket.recv(2048).decode()
            if(message):
                for cName in CLIENTS:
                    cSocket = CLIENTS[cName]["player_socket"]
                    if('wins the game.' in message):
                        gameOver = True
                    cSocket.send(message.encode())
        except:
            pass

def handle_client():
    global CLIENTS
    global FLASH_NUMBER_LIST
    global players_joined
    
    while(True):
        try:
            if len(list(CLIENTS.keys())) >= 2:
                if not players_joined:
                    players_joined = True
                    time.sleep(1)
            if len(FLASH_NUMBER_LIST) > 0:
                random_number = random.choice(FLASH_NUMBER_LIST)
                current_name = None
                try:
                    for cname in CLIENTS:
                        current_name = cname
                        csocket = CLIENTS[cname]["player_socket"]
                        csocket.send(str(random_number).encode())
                    FLASH_NUMBER_LIST.remove(int(random_number))    

                except:
                    del CLIENTS[current_name]
                time.sleep(3)  
        except:
            pass



def accept_connections():
    global SERVER
    global CLIENTS

    while True:
        player_socket,addr= SERVER.accept()  # type: ignore
        player_name = player_socket.recv(1024).decode().strip()
        if( len(CLIENTS.keys())== 0):
            CLIENTS[player_name] = {'player_type':'player_1'}
        else :
            CLIENTS[player_name] = {'player_type':'player_2'}

        
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name
        CLIENTS[player_name]["turn"] = False
        print(f"Connection established with {player_name}:{addr}")
        

        

def setup():
    print("\n\t\t\t\t\t***Welcome to Tambola Game***\n")
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(10)
    print("\t\t\tServer is waiting for the incoming connections")
    thread = Thread(target=handle_client,args=())
    thread.start()
    
    accept_connections()



    

setup()