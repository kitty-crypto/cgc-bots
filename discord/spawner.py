import os
import sys
from random import seed, randint
from datetime import datetime
import discord as Discord
from dbx import dbf
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from logprint import custom_print
from discord import Message

class spawner():
  def __init__(self, discord, channel) -> None:
    seed(datetime.now().timestamp())
    self.__discord = discord
    self.neko_folder = dbf()
    self.__COMMAND_LIST = {
      '!angry': self.__angry,
      '!bless': self.__bless,
      '!blush': self.__blush,
      '!borger': self.__borger,
      '!curse': self.__curse,
      '!drink': self.__drink,
      '!food': self.__food,
      '!gm': self.__gm,
      '!gn': self.__gn,
      '!happy': self.__happy,
      '!hug': self.__hug,
      '!kick': self.__kick,
      '!kiss': self.__kiss,
      '!neko': self.__neko,
      '!pat': self.__pat,
      '!present': self.__present,
      '!punch': self.__punch,
      '!sad': self.__sad,
      '!tickle': self.__tickle,
      '!yawn': self.__yawn
    }
    self.__COMMAND_MAPS = {'!burger': '!borger', '!borgar': '!borger','!gift': '!present', '!smooch': '!kiss', '!cuddle': '!hug'}
    self.__ALLOWED_CHANNELS = [903681954443038761, channel]

  #  def __check_command(self, message) -> bool:
  #    map_comm = lambda comm: self.__COMMAND_MAPS.get(comm) if comm in list(self.__COMMAND_MAPS.keys()) else comm
  #    message_lst = str(message.content).split('!')
  #    for i in range(1, len(message_lst)):
  #      command = f"!{message_lst[i].split('<')[0].strip()}"
  #      if map_comm(command.lower()) in list(self.__COMMAND_LIST.keys()):
  #        return map_comm(command.lower())
  #    return False

  def __check_commandSlash(self, message: str):
    map_comm = lambda comm: self.__COMMAND_MAPS.get(comm) if comm in list(self.__COMMAND_MAPS.keys()) else comm
    message_lst = message.split('!')
    for i in range(1, len(message_lst)):
      command = f"!{message_lst[i].split('?<')[0].strip()}"
      if map_comm(command.lower()) in list(self.__COMMAND_LIST.keys()):
        return map_comm(command.lower())
    return False

  async def spawnSlash(self, command, interaction, target) -> Message:
    command = self.__check_commandSlash(command)
    if command == False: return False
    execute = lambda action, query: action(query)
    user = interaction.user.mention
    channel = interaction.channel
    folder = f"pics/{command}"
    pics = self.neko_folder.listdir(folder)
    options, exts = [file.split('.')[0] for file in pics], [file.split('.')[-1] for file in pics]
    rng = randint(1, len(pics) - 1)
    self.neko_folder.download(f"{folder}/{options[rng]}.{exts[rng]}")
    try:
      with open(f"{folder}/{options[rng]}.{exts[rng]}", 'rb') as pic:
        picture = Discord.File(pic)

        msg = execute(self.__COMMAND_LIST.get(command), [user, target])
        if interaction.channel_id in self.__ALLOWED_CHANNELS:
          message = {"content": msg, "file": picture}
          return message
        else:
          custom_print(f"Spawn called in non-allowed channel: {channel}")
          return None
    except FileNotFoundError:
      custom_print("Tried to get a file from Dropbox that does not exist!")
    self.neko_folder.remove(f"{folder}/{options[rng]}.{exts[rng]}")
    return

  #async def spawn(self, message) -> bool:
  #  command = self.__check_command(message)
  #  if command == False: return False
  #  content = str(message.content)
  #  execute = lambda action, query: action(query)
  #  user = f"<@{str(message.author.id)}>"
  #  target = f"<{content.split('<')[1].split('>')[0]}>" if len(content.split('<')) > 1 else 'None'
  #  channel = message.channel if message.channel.id in self.__ALLOWED_CHANNELS else None
  #  folder = f"pics/{command}"
    #try:
    #  pics = os.listdir(folder)
    #except FileNotFoundError:
    #  return False
    #options, exts = [file.split('.')[0] for file in pics], [file.split('.')[-1] for file in pics]
  #  pics = self.neko_folder.listdir(folder)
  #  options, exts = [file.split('.')[0] for file in pics], [file.split('.')[-1] for file in pics]
  #  rng = randint(1, len(pics) - 1)
  #  self.neko_folder.download(f"{folder}/{options[rng]}.{exts[rng]}")
  #  try:
  #    with open(f"{folder}/{options[rng]}.{exts[rng]}", 'rb') as pic:
  #      picture = Discord.File(pic)
  #      msg = execute(self.__COMMAND_LIST.get(command), [user, target])
  #      try:
  #        await channel.send(msg, file = picture)
  #      except AttributeError:
  #        custom_print(f"Spawn called in non-allowed channel: {message.channel.id}")
  #  except FileNotFoundError:
  #    custom_print("Tried to get a file from Dropbox that does not exist!")
  #  self.neko_folder.remove(f"{folder}/{options[rng]}.{exts[rng]}")
  #  return

  def __angry(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} is angry at {target} — hissing sounds —"
    return f"{user} is angry!, careful!"

  def __bless(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} sends blesses to {target}, Mae the force be with you!"
    return f"{user} feels blessed, Pawlleluja!"

  def __blush(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} blushes at {target}, rawr!"
    return f"{user} blushes, nya!"

  def __borger(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} gives {target} a nice borger, yum!"
    return f"{user} says 'I can has cheezborgar?!'"

  def __curse(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} is cursing {target}. — I wish you get fleas! —"
    return f"{user} is cussing. — Angry cat noises —"

  def __drink(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} gives {target} a drink, purrfect!"
    return f"{user} drinks a big glup!"

  def __food(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} feeds {target}, delicious!"
    return f"{user} wants some food!"

  def __gm(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} says good morning to {target}"
    return f"{user} says good morning to everyone!"

  def __gn(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} says good night to {target}, sleep tight!"
    return f"{user} says good night to everyone! Night night!"

  def __happy(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} is happy when {target} is around, nya nya nya!"
    return f"{user} feels happy! — purrs —"
    
  def __hug(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} hugs {target}, nya!"
    return f"{user} wants some hugs!"

  def __kick(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} kicks {target}. Ouch!"
    return f"{user} kicks the air! — Hyyyyyaa! —"

  def __kiss(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} gives a little kiss to {target}. How sweet!"
    return f"{user} wants some smooches!"

  def __neko(self, users: list) -> str:
    user = users[0]
    return f"{user} spawns nekos!"
  
  def __pat(self, users: list) -> str:
      user = users[0]
      target = users[1]
      if target != None:
        target = target.mention
        return f"{user} gives {target} gentle pats, good Neko!"
      return f"{user} wants pats!"

  def __present(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} gives {target} a present, how purrfect!"
    return f"{user} has a present for someone!"

  def __punch(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} punches {target} owch!"
    return f"{user} is looking for a fight, — who wants some of this?! —"

  def __sad(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} feels sad for {target}, I so sorry! — purrs —"
    return f"{user} is feeling blue!, meow!"

  def __tickle(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} tickles {target}, they can't scape!"
    return f"{user} feels ticklish! nyanyanya!"

  def __yawn(self, users: list) -> str:
    user = users[0]
    target = users[1]
    if target != None:
      target = target.mention
      return f"{user} yawns at {target}, you are boring them!"
    return f"{user} yawns. Are they tired, nya?"