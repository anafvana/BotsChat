import random
import socket
import time
import threading
from bots import all_behaviour

#Empty array so that sometimes activity2 is empty
empty_behaviour = [None]*(int(all_behaviour.__len__()/3))

activity = random.choice(all_behaviour)
activity2 = random.choice(all_behaviour + empty_behaviour)

#Lists which will contain information about connected clients and users
clients = []
users = []

#Target number of users which must be reached for dialogue to start
    #Max 4
target_nr = 4

#Creates TCP server socket
s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_socket.bind(("0.0.0.0", 24242))
s_socket.listen(target_nr)
print("Server is listening...")

#Broadcasts message to all clients
def broadcast(msg, sender=None):
    if type(msg) == str:
        msg = msg.encode()

    for client in clients:
        if client != sender:
            client.send(msg)
    time.sleep(0.1)

#Sends client a request for a username
def addUser(client, address):
    client.send("USRNM".encode())
    #Client will check that username is one of the valid names and send to server
    user = client.recv(1024).decode()

    #If bot hasn't already been initialised, add it
    if user not in users:
        print(f"User: {user}\n")
        users.append(user)
        clients.append(client)
        client.send("\nYou are now connected to the server".encode())
        broadcast(f"\n{user} has joined the chat", client)
        time.sleep(0.3)
        if clients.__len__() < target_nr:
            broadcast(f"\n{clients.__len__()} clients connected. Program will start when {target_nr} are connected")
        else:
            broadcast(f"\n{clients.__len__()} clients connected. Program is starting...\n")
        time.sleep(0.5)
    #Else, close connection
    else:
        client.send(f"\nDo you think you can clone {user}? Outrageous! Try again, charlatan.".encode())
        client.send("You've been kicked out".encode())
        print(f"Duplicated user: {user}")
        print(f"Disconnecting from {str(address)}")
        client.close()

#Kicks out all users
def kickOutAll():
    broadcast("\nYou've been kicked out")

    #Clears lists
    users.clear()
    clients.clear()
    time.sleep(0.5)
    #Closes socket and server instance
    s_socket.close()
    time.sleep(0.5)
    quit()

#Sends activity suggestion(s) and receives answers from bots
def poll():
    if activity2 == None:
        msg = f"Dictator suggested: {activity} "
    else:
        msg = f"Dictator suggested: {activity} or {activity2}"

    for client in clients:
        client.send(msg.encode())
    for client in clients:
        msg = client.recv(1024)
        time.sleep(0.2)
        broadcast(msg, client)

#"Main" function: listens for connections and starts chat when it is time
def connect():
    #On the lookout for connections while the target number isn't reached
    while clients.__len__() < target_nr:
        try:
            #Establishing connection with client upon request
            client, address = s_socket.accept()
            print(f"Connected to {str(address)}")

            #Gets username. If valid, adds client to a list of clients. Else, closes the connection
            addUser(client, address)
        except KeyboardInterrupt:
            print("\nIt's rude not to say \"bye\". Everyone has been kicked out.")
            kickOutAll()
        except:
            print ("\nThe world is a mysterious place and a mysterious error has occurred.")
            kickOutAll()

    #Starts chat when the target number is reached
    if clients.__len__() == target_nr:
        print("Target number reached!")

        try:
            #Starts message exchange on separate thread   
            thread = threading.Thread(target=poll)
            thread.start()
            thread.join()

            #Once all bots have had a say, the dictator kicks in and kicks everybody out because of the audacity of challenging their almighty power
            broadcast(f"Dictator said: Well, guess what? I am the dictator and I say we are {activity}ing! Accept or DIE!!!!")
            time.sleep(1)
            print("\nThis conversation is over.")
            kickOutAll()
        except KeyboardInterrupt:
            print("\nIt's rude not to say \"bye\". Everyone has been kicked out.")
            kickOutAll()
        except BrokenPipeError:
            print("Broken pipe.")
        except:
            print ("Bye...")
            kickOutAll()

#Effectively runs the server
connect()