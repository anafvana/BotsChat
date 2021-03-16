import random
import socket
import time
import threading
from bots import checkIfBot
from socket import SHUT_RDWR

#TODO Remove
activity = "work"
activity2 = None

clients = []
users = []
target_nr = 3
#TODO: Change to 5

#Creates TCP server socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_socket.bind(("0.0.0.0", 24242))
s_socket.listen(target_nr)
s_socket.settimeout(180)
print("Server is listening... But not for long! \nYou have 3 minutes, the clock is ticking.")

#Broadcasts message to all clients
def broadcast(msg):
    if type(msg) == str:
        msg = msg.encode()

    for client in clients:
        client.send(msg)
    time.sleep(0.1)

def pool():
    for client in clients:
        msg = client.recv(1024)
        time.sleep(0.1)
        broadcast(msg)

#Sends client a request for a username
def addUser(client):
    print("In addUser")
    client.send("USRNM".encode())
    #Client will check that username is one of the valid names and send to server
    user = client.recv(1024).decode()
    print(f"User: {user}")

    #If bot hasn't already been initialised, add 
    if user not in users:
        users.append(user)
        clients.append(client)
        client.send("\nYou are now connected to the server".encode())
        time.sleep(0.1)
        broadcast(f"\n{user} has joined the chat")
        time.sleep(0.1)
        if clients.__len__() < target_nr:
            broadcast(f"\n{clients.__len__()} clients connected. Program will start when {target_nr} are connected")
        else:
            broadcast(f"\n{clients.__len__()} clients connected. Program is starting...")
        time.sleep(0.5)
    #Else, close connection
    else:
        client.send(f"\nDo you think you can clone {user}? Outrageous! Try again, charlatan.".encode())
        client.close()

def fetchUser(client):
    i = clients.index(client)
    return users[i]

def botteraction(client):
    msg = checkIfBot(fetchUser(client), activity, activity2)
    broadcast(msg)
    pool()

def kickOutAll():
    broadcast("You've been kicked out")
    for client in clients:
        clients.remove(client)
        users.remove(fetchUser(client))
        client.shutdown(SHUT_RDWR)
        client.close()        
    time.sleep(2)
    quit()

#"Main" function: listens for connections and starts chat when it is time
def connect():
    while True:
        try:
            #Establishing connection with client upon request
            client, address = s_socket.accept()
            print(f"Connected to {str(address)}")

            #Gets username. If valid, adds client to a list of clients. Else, closes the connection
            addUser(client)

            #When program reaches its target number of users, starts message exchange
            if clients.__len__() == target_nr:
                print("Target number reached!")
                while True:
                    msg = "start"
                    if msg == "start":
                        thread = threading.Thread(target=botteraction, args=(client, ))
                        thread.start()
                        thread.join()
                    elif msg == "quit":
                        broadcast("Chatrooom is closing.")
                        kickOutAll()
        except KeyboardInterrupt:
            print("\nIt's rude not to say \"bye\". Everyone has been kicked out.")
            kickOutAll()
        except socket.timeout:
            print("\nIt's just too little too late, a little too wrong, and I can't wait. \n-JoJo")
            kickOutAll()
        except BrokenPipeError:
            continue
        except:
            print ("\nThe world is a mysterious place and a mysterious error has occurred.")
            kickOutAll()

connect()