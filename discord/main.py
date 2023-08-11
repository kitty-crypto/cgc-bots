import asyncpraw
import discord
import os
import sys
from questions_updater import questionFinder
from this_is_the_mae import thisIsTheMae
from spawner import spawner
from daily_task import daily_task as dt
from message_whacker import message_whack
from maeAI import maeAI
from nft_lookup import nftLookup
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from database import database

TOKEN = os.environ['discord_key_mae']  # Discord token ID for bot
reddit = None
client = discord.Client(intents=discord.Intents.all())  # Defining Discord Client
questions = None
mae = thisIsTheMae(client)  # TITM counter object
#nekoSpawn = spawner(client, 911445338295001151)
daily_task = dt(client)
mw = message_whack(client)
mae_ai = maeAI(client, (1019956566360871002, 845739075835002930),  1020262410675822633)
#lookup = nftLookup(client)
db = database("database.db")
main_channel = 845739075835002930

async def initialise_reddit():
  global reddit
  global questions
  reddit = asyncpraw.Reddit(  # Initialising reddit bot
    client_id='GPs6wxXUncfEVH6wAn2KSQ',
    client_secret=os.environ['GPs6wxXUncfEVH6wAn2KSQ'],
    username='this_is_the_mae',
    password=os.environ['this_is_the_mae'],
    user_agent="<ReplyCommentBot1.0>")

@client.event
async def on_ready():
  await initialise_reddit()
  global questions 
  questions = questionFinder(client, reddit)  # Questions object
  print('Logged in as {0.user}'.format(client))  # Tell user that the bot is logged in
  await mae.update_presence()  # Update the TITM counter with the latest DB count
  while True:
    await questions.question_updater()  # Run the questions fetch routine
    
@client.event
async def on_message(message):  # On every message
  if message.author == client.user: return False
  if  message.channel.id == main_channel:
    dt_db = db['daily_task']
    dt_db["last_msg"] += 1
    db["daily_task"] = dt_db    
  await daily_task.schedule_daily_task(db['daily_task']['last_msg'])
  await mae.check_messages(message)  # Run message fetch routine
  #await nekoSpawn.spawn(message)
  await mw.whack_message(message)
  await mae_ai.respond(message)
  #await lookup.check_message(message)
  return True
  
client.run(TOKEN)
