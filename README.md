# Using the chatbot

To use this chat, you will need:

- One instance of the server
- Four running bots
- One running dictator

## Running the files

### Server

Start the server with python3 server.py

### Clients

Start the bots with python3 client.py \[IP\] \[port\] \[OPTIONAL: bot\]

Start the dictator with python3 client.py \[IP\] \[port\] \[OPTIONAL: dictator\]

If you do not insert the third argument, you will be prompted to choose a user.

## Options

### Users

Your user options are:

- dictator (interactive)
- alice (bot)
- beth (bot)
- bob (bot)
- chuck (bot)

### Activities

In dictator mode, you may choose one or two activities to suggest. The options are:

- bad behaviour = ["fight", "kill", "shout", "murder", "bicker", "saw", "yell", "stalk", "scream", "destroy", "complain", "steal"]
- good behaviour = ["hug", "craft", "walk", "play", "sing", "sew", "talk", "eat", "sleep", "work", "laugh", "cry", "dream", "text"]
  To insert two activities, simply write the verbs separated by a space.

## Closing the chatbot

The program should close itself once all bots have had their say. In case it does not, use ctrl+c / cmd+c to quit.
