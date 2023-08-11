import os
import discord
from clock import clock

TOKEN = os.environ.get('discord_key_clock')  # Discord token ID for bot
client = discord.Client(intents=discord.Intents.default())  # Defining Discord Client
mae_clock = clock(client)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))  # Tell user that the bot is logged in
  while True:
    await mae_clock.start()

client.run(TOKEN)
