import socket
from threading import Thread

SERVER = None
IP_ADDRESS = "127.0.0.1"
PORT = 6000

CLIENTS = {}

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
    accept_connections()

setup()