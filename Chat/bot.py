# Import necessary 
import datetime
import random

# Answer based on predefined rules
def get_ans(req):
    req = req.lower()

    if 'hi' in req or 'hello' in req:
        return "Hello!"
    elif 'what' in req and 'time' in req:
        now = datetime.datetime.now()
        return "It's %s:%s" % (now.hour, now.minute)
    elif 'how' in req and 'you' in req:
        return "I'm doing great!"
    elif 'weather' in req:
        return "It's such a great sunny day!"
    elif 'temperature' in req:
        return "It's about 23 degrees."
    elif 'color' in req:
        return "It's blue."
    elif 'song' in req:
        return "'Courage to change' by Sia."
    elif 'car' in req:
        return "BMW 330i G20."
    elif 'university' in req or 'itmo' in req:
        return "ITMO university!"
    else:
        return "It's a pleasure to meet you!"

# List of arbitrary sentences
sentences = ["How are you doing?",
            "Good to see you!",
            "I'm always here.",
            "Ask me anything.",
            "What a beautiful day",
            "Hello!"
            ]

# Get random sentence
def chatting():
    return random.choice(sentences)