import discord
import os
from pricebot import pricebot as pb
from chart import priceChart as pc

TOKEN = os.environ['discord_key_feline']  # Discord token ID for bot
client = discord.Client(intents=discord.Intents.all())  # Defining Discord Client
feline = pb(client, 'https://api.coinbrain.com/public/coin-info', '0x79ebc9a2ce02277a4b5b3a768b1c0a4ed75bd936', 56)
chartBot = pc([845739075835002930], client)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))  # Tell user that the bot is logged in
  await feline.update_presence()  # Update the price

@client.event
async def on_message(message):  # On every message
  await feline.update_presence()
  await chartBot.requestChart(message)


client.run(TOKEN)
