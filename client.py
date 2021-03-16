import socket, sys
import time
import threading
from bots import checkIfBot

users = ["Dictator", "Alice", "Beth", "Bob", "Chuck"]
#TODO Remove
activity = "work"
activity2 = None

def checkValidUser(inp):
    while inp == None or inp.lower().capitalize() not in users:
        print(f"Please choose a user: \"{users[0]}\" (to send messages), \"{users[1]}\" (bot), \"{users[2]}\" (bot), \"{users[3]}\" (bot) or \"{users[4]}\" (bot). Do not include quotation marks.")
        inp = input("User: ")
    return inp.lower().capitalize()

def prevBot(user):
    i = users.index(user)
    if i > 1:
        return users[i-1]
    else:
        return users[users.__len__()-1]

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
            to_split = user+" said:"
            if msg.startswith(to_split):
                print("You said:" + msg[len(to_split):])
        elif msg.startswith(users[0]):
            msg = f"{user} said: {checkIfBot(user, activity, activity2)}"
            c_socket.send(msg.encode())
        elif msg=="You've been kicked out":
            print(msg)
            print("Bye...")
            c_socket.close()
            quit()
        elif msg!="":
                print(msg)
    except:
        c_socket.close()
        break