import os #for token
import discord #for getting Client 
import requests #http request
import json #http request responds in json
import random #randomly select from list
from replit import db #to save in database

client = discord.Client()

#if the user says sad_words
sad_words = ["sad","depressed","unhappy","miserable","depressing","cry","angry"]

#bot responds with starter_encouragements
starter_encouragements = ["cheer up!","don't be sad!","hang on!","you'll get through this!","you're a good person"]

#bot only responds to trigger words if true (feature can be operated in dicord by user)
if "responding" not in db.keys():
  db["reponding"] = True

#getting quotes from http request 
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+"-"+json_data[0]['a']
  return quote

#update encouraging words based on user input
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]= encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

#message displayed on connecting the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
#if message is from bot, return
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$hello'):
        await message.channel.send("Hello!")
    
    #respond from get_quotes
    if msg.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)
    
    #setting whether bot can respond to words which can be set in discord itself
    if msg.startswith("$responding"):
      value = msg.split("$responding ",1)[1]
      if value.lower == "true":
        db["responding"] = True
        await message.channel.send("Responding is ON")
      else:
        db["responding"] = False
        await message.channel.send("Responding is OFF")

    if db["responding"]:
      options=starter_encouragements
      if "encouragements" in db.keys():
          options = options.append(list(db["encouragements"])[0])
      if any(word in msg for word in sad_words):
          await message.channel.send(random.choice(starter_encouragements))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(list(encouragements))

    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(list(encouragements))

    


    
    
    
        
my_secret = os.environ['Bot']
client.run(my_secret)

