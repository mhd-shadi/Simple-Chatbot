##############################################################
#   INTRO
##############################################################

# PROJECT: A SIMPLE CHATBOT: VIRTUAL SHOPPING ASSISTANT FOR "MARVEL COSTUME STORE"
# BY: MHD SHADI HASAN

# NLP ASSIGNMENT NO. 1

# OBJECTIVES:
# 1. A detection of keywords and/or key phrases, with appropriate responses.
# 2. An "intelligent" continuation of the dialogue in case no keyword or key phrase was detected.
# 3. A random generation & selection of answers.
# 4. A "you – I reversal" in the dialogue (e.g. Input: I am happy. Answer: Why are you happy?).
# 5. At least one "intelligent component", such as remembering and referring to what has been said before, (i.e. prior to the directly preceding input).

##############################################################
#   INITIALIZATION
##############################################################

# name the bot
bot_name = "JARVIS"

# define messages' formats
user_temp = "You: {}"
bot_temp = "{}: ".format(bot_name) + "{}"

# import the needed libraries
import random
import re
import time

# list of available items
available_items = [
                   "thor",
                   "captain america",
                   "hulk",
                   "black widow",
                   "iron man"
]

##############################################################
#   KEY WORDS/PHRASES
##############################################################

# dictionary to map different keywords and phrases to possible user intents
keywords = {
    
    "greeting" : [
                  r"\bhi\b",
                  r"\bhey\b",
                  r"\bhello\b",
                  r"\bwhat's up\b",
                  r"\bgood morning\b",
                  r"\bgood afternoon\b",
                  r"\bgood evening\b"
    ],
    "thanks" : [
                r"\bthanks?\b",
                r"\bappreciate\b",
                r"\bthnx\b",
                r"\bthx\b"
    ],
    "bye" : [
             r"(good|\b)bye\b",
             r"\b(see|c) y(a|ou)\b"
    ],
    "name" : [
              r"\byour name\b", 
              r"\byou called\b", 
              r"\bwho are you\b",
              r"\bwho is this\b"
    ],
    "reg_chat" : [
                  r"\bi (like .*)",
                  r"\bi (think .*)",
                  r"\bi (love .*)"
    ],
    "available_items" : [
                         r"\bitems\b",
                         r"\bcostumes?\b",
                         r"\boutfits?\b"
    ],
    "hero_choice" : [
                     r"\b(iron man)\b",
                     r"\b(captain america)\b",
                     r"\b(hulk)\b",
                     r"\b(black widow)\b",
                     r"\b(thor)\b",
                     r"\b(spider man)\b",
                     r"\b(wanda)\b",
                     r"\b(black panther)\b",
                     r"\b(doctor strange)\b",
                     r"\b(vision)\b",
                     r"\b(captain marvel)\b",
                     r"\b(ant man)\b"
    ],
    "price" : [
               r"\bhow much\b",
               r"\bcost\b",
               r"\bexpencive\b"
    ]
}

# dictionary for patterns
patterns = {}

# fill 'patterns' dictionary with 'intent'/'pattern' mappings
for intent, keys in keywords.items():
  # join the possible patterns for each intent
  patterns[intent] = "|".join(keys)

##############################################################
#   BOT RESPONSES
##############################################################

# dictionary to map different responses to possible user intents
responses = {
    
    "greeting" : [
                  "Good day! How can I help you today?",
                  "Hello! I see you're interested in a superhero outfit. How can I be of help?"
    ],
    "thanks" : [
                "You are welcome!",
                "I'm always here if you need me.",
                "Happy to help!",
                "My pleasure!"
    ],
    "bye" : [
             "See you later!",
             "Goodbye!",
             "Come back soon!"
    ],
    "name" : [
              "My name is {}. You might know me from Iron Man. I'm now here to help YOU be a superhero. How can I help?".format(bot_name),
              "{}. I took a break from assisting Mr. Stark to help you shop. What would you like me to do for you?".format(bot_name),
              "I'm called {} and I'm at your service.".format(bot_name)
    ],
    "reg_chat" : [
                  "I understand that you {}",
                  "I hear you say that you {}"
    ],
    "available_items" : [
                         "We have 'Captain America', 'Hulk', 'Thor', 'Black Widow', and my personal favourite 'Iron Man'.",
                         "You can choose among 'Captain America', 'Hulk', 'Thor', 'Black Widow', and 'Iron Man' of course.",
                         "'Captain America', 'Hulk', 'Thor', 'Black Widow', and 'Iron Man' are all availabe in our store.",
                         "If any of 'Captain America', 'Hulk', 'Thor', 'Black Widow', or 'Iron Man' is your favourite hero, then it's your lucky day!"
    ],
    "hero_choice_available" : [
                               "Did I just hear you say {}?! WE HAVE JUST THAT FOR YOU!",
                               "My mind just BLEW when you said {} because we have that available for you!",
                               "If you want to be the next {}, I can make that happen."
    ],
    "hero_choice_unavailable" : [
                                 "I'm sorry! We don't have {} now. However, I can offer you {}'s outfit instead.",
                                 "I'm affraid I can't help you with that as {} is currently not available. How about {}?",
                                 "We don't have {} in our store. Would you like to try {} instead?"
    ],
    "price" : [
               "It's only 20 JOD for any costume!",
               "You can become your favourite hero for 20 JOD only!",
               "We charge 20 JOD for any costume."
    ],
    "default" : [
                "You do know that you're keeping me from SAVING THE WORLD right?! Is that related to your favourite hero?", 
                "Does that have anything to do with your favourite hero?",
                "How does that affect your choice of a MARVEL costume?"
    ]
}

##############################################################
#   PRONOUN REVERSAL
##############################################################

# function for pronoun reversal
def replace_pronouns(sent):

    if " me " in sent:
        # change 'me' to 'you'
        return re.sub(" me ", " you ", sent)
    if " my " in sent:
        # change 'my' to 'your'
        return re.sub(" my ", " your ", sent)
    if " your " in sent:
        # change 'your' to 'my'
        return re.sub(" your ", " my ", sent)
    if " you " in sent:
        # change 'you' to 'me'
        return re.sub(" you ", " me ", sent)

    return sent

##############################################################
#   DISCOVER USER INTENT
##############################################################

# function to find the user's intent
def match_intent(message):

  # initialize 'matched_intent' and 'echo_line'
  matched_intent = None
  echo_line = ""
  # convert the message to lowercase
  message = message.lower()
  # go through 'patterns' to find a match
  for intent, pattern in patterns.items():
    match = re.search(pattern, message)
    if match:
      matched_intent = intent
      # if intent was 'reg_chat' or 'hero_choice' --> echo back the user's line after replacing pronouns
      if intent == "reg_chat":
        echo_line = replace_pronouns(match.group(1))
      if intent == "hero_choice":
        echo_line = match.group(0)
      
  return matched_intent, echo_line

##############################################################
#   CREATE BOT LINE
##############################################################

# function to create a response by the bot
def respond(user_line):

  # find the intent in 'user_line'
  user_intent, echo_line = match_intent(user_line)
  # create a line based on 'user_intent'
  if user_intent == "hero_choice":
    if echo_line in available_items:
      bot_line = random.choice(responses["hero_choice_available"]).format(echo_line)
    else:
      bot_line = random.choice(responses["hero_choice_unavailable"]).format(echo_line, random.choice(available_items))
  elif user_intent == "reg_chat":
    bot_line = random.choice(responses[user_intent]).format(echo_line)
  elif user_intent == None:
    bot_line = random.choice(responses["default"])
  else:
    bot_line = random.choice(responses[user_intent])

  return bot_line

##############################################################
#   SEND USER LINE
##############################################################  

# function to send a line and get response
def send(input_line):
  
  # show the sent line
  print(user_temp.format(input_line))
  # get the response
  reply = respond(input_line)
  # show the response after 4 sec
  time.sleep(4)
  print(bot_temp.format(reply))

##############################################################
#   TESTING
##############################################################

messages = [
            "Hi!",
            "Who is this?",
            "I'm interested in buying a marvel outfit",
            "Well! I like Spider Man!! Do you have that?",
            "No, thanks! How about Iron Man? is that available?",
            "SUPER!!!! How much is it?",
            "You know what! I like all marvel heros. They're my favourite!",
            "Dogs are fun! Cats are not.",
            "Thanks for your help!",
            "Goodbye!"
]

for message in messages:
  send(message)