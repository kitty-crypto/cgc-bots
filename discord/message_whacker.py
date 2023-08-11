import sys
import os
import discord
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from database import database
from logprint import custom_print

class message_whack:
  def __init__(self, client):
    self.client = client
    self.db = database('database.db')

  async def whack_message(self, message):
    if await self.check_mssg(message):
      await message.delete()

  async def check_mssg(self, message):
    if message.channel.id not in self.db.get('channels')['whack']: return False
    return True
    #if message.content[0] == '!': return False
    #return True