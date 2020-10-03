import socket
from _thread import *
from player import Player
import pickle

server = "192.168.1.8"
port = 5555 #safe port to use

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #opens up the port, lets clients connect (has 1 optional arg - empty means unlimited people can connect)
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]

def threaded_client(conn, player): #threaded function - don't have to wait for this function to end before continuing while loop
    conn.send(pickle.dumps(players[player]))
    reply = ""

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True: #this will continuously look for connections
    conn, addr = s.accept() #an object - accept any incoming connections
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
