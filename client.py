import socket, sys
import time
import threading
from bots import checkIfBot

proceed = True
users = ["dictator", "alice", "beth", "bob", "chuck"]

def checkValidUser(inp):
    while inp == None or inp.lower() not in users:
        print(f"Please choose a user: \"{users[0]}\" (to send messages), \"{users[1]}\" (bot), \"{users[2]}\" (bot), \"{users[3]}\" (bot) or \"{users[4]}\" (bot). Do not include quotation marks.")
        inp = input("User: ")
    return inp


try:
    hostIP = sys.argv[1]
    hostPort = int(sys.argv[2])
except:
    proceed = False
    print("Please include the following arguments, in order: [host IP] [port 24242] [OPTIONAL: user]")
    print(f"Write \"{users[0]}\" for sending messages. For the bots, choose \"{users[1]}\", \"{users[2]}\", \"{users[3]}\" or \"{users[4]}\"")

try:
    tmp_user = sys.argv[3]
except:
    tmp_user = None
user = checkValidUser(tmp_user)

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect((hostIP, hostPort))

while True:
    try:
        msg = c_socket.recv(1024).decode()
        if msg == "USRNM":
            c_socket.send(user.encode())
        elif msg.startswith(user):
            to_split = user+" says:"
            if msg.startswith(to_split):
                print("You said:" + msg[len(to_split):])
        elif msg=="You've been kicked out":
            print(msg)
            print("Bye...")
            c_socket.close()
            quit()
        else:
            print(msg)
    except:
        c_socket.close()
        break