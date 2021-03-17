import socket, sys
import time
import threading
from bots import actBot

users = ["Alice", "Beth", "Bob", "Chuck"]

#Check if the input user is a valid value
def checkValidUser(inp):
    while inp == None or inp.lower().capitalize() not in users:
        print(f"Please choose a bot: \"{users[0]}\", \"{users[1]}\", \"{users[2]}\" or \"{users[3]}\". Do not include quotation marks.")
        inp = input("User: ")
    return inp.lower().capitalize()

#Fetches arguments used to start the program
try:
    hostIP = sys.argv[1]
    hostPort = int(sys.argv[2])
except:
    proceed = False
    print("Please include the following arguments, in order: [host IP] [port 24242] [OPTIONAL: user]")
    print(f"Choose \"{users[0]}\", \"{users[1]}\", \"{users[2]}\" or \"{users[3]}\"")
    quit()

#Checks if user was inserted and confirms validity
try:
    tmp_user = sys.argv[3]
except:
    tmp_user = None
user = checkValidUser(tmp_user)

#Creates socket
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    c_socket.connect((hostIP, hostPort))
except ConnectionRefusedError:
    print("ERROR! Have you remembered to start the server?")
    quit()
except:
    print("An error occurred. Try again.")

#"Main" listen function
def listen():
    #Continuously listens for messages from the server
    while True:
        try:
            msg = c_socket.recv(1024).decode()
            
            #When the request for the username comes, send username
            if msg == "USRNM":
                c_socket.send(user.encode())

            #When the prompt-message from the dictator comes, bot outputs its message
            elif msg.startswith(f"Dictator suggested: "):
                words = msg.split(' ')
                activity = words[2]
                try:
                    activity2 = words[4]
                except:
                    activity2 = None
                print(msg)
                bot_msg = actBot(user, activity, activity2)
                print(f"You said: {bot_msg}")
                c_socket.send(f"{user} said: {bot_msg}".encode())
                print("Sent")

            #Handles being kicked out by the server
            elif msg=="\nYou've been kicked out":
                print(msg)
                print("Bye...")
                c_socket.close()
                quit()

            #Prints any non-empty messages that do not meet the previous conditions
            elif msg!="":
                print(msg)
        except:
            c_socket.close()
            quit()
            break

listen()