import random

bad_behaviour = ["fight", "kill", "shout", "murder", "bicker", "saw", "yell", "stalk", "scream", "destroy", "complain", "steal"]
good_behaviour = ["kiss", "craft", "walk", "play", "sing", "sew", "talk", "eat", "sleep", "work", "laugh", "cry", "dream", "text"]
all_behaviour = bad_behaviour + good_behaviour


def alice(a, b = None):
    if b != None:
        return "{} and {} both sound great!".format(a+"ing", b+"ing")
    else:
        return "I think {} sounds wonderful!".format(a+"ing")
    
def bob(a, b = None):
    if b != None:
        return "I'm not so sure about {}, but we could give {} a try.".format(a+"ing", b+"ing")
    else:
        return "So it's like that now? We only get one option from the great dictator? I say no to {}!".format(a+"ing")
    
def beth(a, b = None):
    suggestion = random.choice(all_behaviour)
    while (suggestion == a) or (suggestion == b):
        suggestion = random.choice(all_behaviour)
    
    if b == None:
        return "Sure, {} is an option. But what if we do some {}?".format(a+"ing", suggestion+"ing")
    else: 
        return "Sure, {} and {} are options. But what if we do some {}?".format(a+"ing", b+"ing", suggestion+"ing")
    
def chuck(a, b = None):
    out = ""
    if good_behaviour.__contains__(a) and b!=None:
        out += "{} sounds LAME ".format(a+"ing")
        if b != None and bad_behaviour.__contains__(b):
            out += "but {} sounds just like my jam.".format(b+"ing")
        else:
            out += "and so does {}".format(b+"ing")
    elif bad_behaviour.__contains__(a) and b!=None:
        out += "You got me at {}! Let's go".format(a+"ing")
    else:
        out += "{}? Sounds like what a loser would do.".format(a+"ing")
    return out

botsDict = {'Alice':alice, 'Beth':beth, 'Bob':bob,'Chuck':chuck}

def actBot(inp, activity, activity2 = None):
    inp = str(inp).lower().capitalize()
    if inp in botsDict:
        return botsDict[inp](activity, activity2)
    else:
        out = "I am trying to do wrong things with this program. This is an automatic self-shaming message."
        return out