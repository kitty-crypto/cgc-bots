import sys
import os
from datetime import datetime
from dbx import dbf
import discord
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from database import database
from logprint import custom_print

class thisIsTheMae: # Class that has the message getching commands. Counts TITM occurrances in the server
  def __init__(self, client): # Only needs the client for initialisation
    self.client = client # Define client
    self.neko_folder = dbf()
    self.prompts = {
      'this is the mae': self.__update_counter,
      'good bot': self.__good_bot,
      'when moon': self.__w_moon,
      'when burn': self.__w_burn,
      'when 10x': self.__w_10x,
      'when lambo': self.__w_lambo,
      'when pump': self.__w_pump,
      '!updatedt': self.__update_daily_task
    }
    self.execute = lambda action, query: action(query)
    self.db = database('database.db')
  '''  
  async def __update_titm_roles(self, server_id = 845738053259100171): # Updates the roles of top 3 TITM users
    server = self.client.get_guild(server_id) # Gets the server ID where the roles are
    top = discord.utils.get(server.roles, name = 'Top Mae') # First place role
    vice = discord.utils.get(server.roles, name = 'Vice Mae') # Second place role
    also = discord.utils.get(server.roles, name = 'Also Mae') # Third place role
    first =  list(self.db['titm'].get('rank').keys())[0] # Who is currently on first place
    second = list(self.db['titm'].get('rank').keys())[1] # Who is currently on second place
    third =  list(self.db['titm'].get('rank').keys())[2] # Who is currently on third place
    #CHECKS#
      # FIRST PLACE
    if self.db['titm']['top_users']['0'] != first: # If current first place is different from the on the database
      old = await server.fetch_member(int(self.db['titm'].get('top_users')['0']))
      new = await server.fetch_member(int(first))
      await old.remove_roles(top) # remove the role from previous first place holder
      await new.add_roles(top) # add it to new first place holder
      self.db['titm']['top_users']['0'] = first # update database
      # SECOND PLACE
    if self.db['titm']['top_users']['1'] != second: # see above
      old = await server.fetch_member(int(self.db['titm'].get('top_users')['1']))
      new = await server.fetch_member(int(second))
      await old.remove_roles(vice)
      await new.add_roles(vice)
      self.db['titm']['top_users']['1'] = second
      # THIRD PLACE
    if self.db['titm']['top_users']['2'] != third: # see above
      old = await server.fetch_member(int(self.db['titm'].get('top_users')['2']))
      new = await server.fetch_member(int(third))
      await old.remove_roles(also)
      await new.add_roles(also)
      self.db['titm']['top_users']['2'] = third
  '''
  
  def __sort_rank(self, ranking: dict) -> dict: # takes a dictionary with format {user_id: [score, timestamp]} and maps it to list [[[user_id],[score, timestamp]], ...] for sorting.
    lb_list = list(map(list, ranking.items()))
    for i in range(len(lb_list) - 1): # bubble sort emlements base on dict_list[i][1][0] (score)
      for j in range(i + 1, len(lb_list)):
        if lb_list[i][1][0] < lb_list[j][1][0]:
          lb_list[i], lb_list[j] = lb_list[j], lb_list[i]
    return dict(lb_list) # convert the list back into a dict and return sorted dictionary

  def __emoji_scores(self, score): # Returns a emoji if place of user is 1, 2 or 3
    if score == 1:
      return "🥇 - "
    elif score == 2:
      return "🥈 - "
    elif score == 3:
      return "🥉 - "
    else:
      return f"  {score} - " # returns just the score if not

  def __achiev_points(self, points): # Achievements given to users when their score reaches certain number
    if points == 42:
      return "42. 🚀 The question of life, the Universe and everything!"
    elif points == 69:
      return "69. 👌 Nice"
    elif points == 101:
      return "101. 📓 Mae: The basics"
    elif points == 404:
      return "404. ❌ Achievement not found."
    elif points == 404:
      return "420. 🌿 Blaze it."
    elif points == 666:
      return "666. 😈 Evil Mae."
    elif points == 404:
      return "9001. 🐱‍👤 IT'S OVER 9000!"
    else:
      return str(points)

  def __rank_to_msg(self, ranking) -> str: # Converts a dictionary into a string for ranking message
    output = f"~°~°~°~(≈uωu≈)~°~°~°~\n  Current Count: {str(self.db.get('titm')['score'])}\n~°~°~°~(≈uωu≈)~°~°~°~\n"
    for i, val in enumerate(ranking.keys()):
      score = self.__achiev_points(list(ranking.values())[i][0])
      if i > 19: break  #Only show first 20 users
      output += f"{self.__emoji_scores(i+1)}<@{val}>: {score}\n"
    if len(ranking.keys()) > 19: # Show last user if there are more than 20
      output += f"                       ...\n"
      score = self.__achiev_points(list(ranking.values())[-1][0])
      last = self.__emoji_scores(len(list(ranking.keys())))
      output += f"{last}<@{list(ranking.keys())[-1]}>: {score}"
    return output

  async def __update_presence(self): # Updates the status of the bot
    sum_scores = lambda dictionary: sum(dictionary[key][0] for key in dictionary)
    titm_dict = self.db['titm']
    titm_dict['score'] = sum_scores(self.db['titm']['rank'])
    #print(titm_dict['score'])
    self.db['titm'] = titm_dict
    titm = self.db.get('titm')['score'] # Fetch the count from self.db
    titm_rank_channel = await self.client.fetch_channel(self.db['titm']['rank_channel'])
    if titm == 69:
      counter = f"👌 NICE {titm} 👌"
      self.neko_folder.download(f"pics/memes/69.jpg")
      with open(f"pics/memes/69.jpg", 'rb') as pic:
        picture = discord.File(pic)
      await titm_rank_channel.send('Milestone achieved - 69: Nice!', file = picture)
      self.neko_folder.remove(f"pics/memes/69.jpg")
    elif titm == 101:
      counter = f"📚📓 Mae {titm}: The basics 📚📓"
      self.neko_folder.download(f"pics/memes/101.jpg")
      with open(f"pics/memes/101.jpg", 'rb') as pic:
        picture = discord.File(pic)
      await titm_rank_channel.send('Milestone achieved - Mae 101: The basics.', file = picture)
      self.neko_folder.remove(f"pics/memes/101.jpg")
    elif titm == 404:
      counter = f"❌{titm}"
      self.neko_folder.download(f"pics/memes/404.jpg")
      with open(f"pics/memes/404.jpg", 'rb') as pic:
        picture = discord.File(pic)
      await titm_rank_channel.send('Milestone achieved - 404: Achevement not found.', file = picture)
      self.neko_folder.remove(f"pics/memes/404.jpg")
    elif titm == 420:
      counter = f"🌿🌿🌿 {titm}"
      self.neko_folder.download(f"pics/memes/420.jpg")
      with open(f"pics/memes/420.jpg", 'rb') as pic:
        picture = discord.File(pic)
      await titm_rank_channel.send('Milestone achieved - 420: Blaze it.', file = picture)
      self.neko_folder.remove(f"pics/memes/420.jpg")
    elif titm == 666:
      counter = f"😈😈😈 {titm}"
      self.neko_folder.download(f"pics/memes/666.jpg")
      with open(f"pics/memes/666.jpg", 'rb') as pic:
        picture = discord.File(pic)
      await titm_rank_channel.send('Milestone achieved - 666: Preparing to Summon Cathulhu.', file = picture)
      self.neko_folder.remove(f"pics/memes/666.jpg")
    elif titm == 9001:
      counter = f"It's over 9000!: {titm}"
      self.neko_folder.download(f"pics/memes/9001.gif")
      with open(f"pics/memes/9001.gif", 'rb') as pic:
        picture = discord.File(pic)
      await titm_rank_channel.send("Milestone achieved - It's over 9000!", file = picture)
      self.neko_folder.remove(f"pics/memes/9001.gif")
    else:
      counter = f'This is the Mae: {titm}' # Create string for presence
    await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=counter))

  async def __update_counter(self, message, cooldown = 60): # Updates the counter message (presence of the bot)
    if str(message.author.id) == '645343657075146772': return False # Do not count XP bot
    now = int(datetime.now().timestamp())
    try:
      sum_scores = lambda dictionary: sum(dictionary[key][0] for key in dictionary)
      rank_dict = self.db.get('titm')['rank']
      user_score = rank_dict.get(str(message.author.id))
      if user_score == None: user_score = [0, now - cooldown - 1]
      if user_score[1] > now - cooldown: return False
      user_score[0] += 1
      user_score[1] = now
      rank_dict[str(message.author.id)] = user_score
      rank_dict = self.__sort_rank(rank_dict)
      titm_dict = self.db['titm']
      titm_dict['rank'] = rank_dict
      titm_dict['score'] = sum_scores(titm_dict['rank'])
      self.db['titm'] = titm_dict
      #print(self.db['titm']['rank'])
    except KeyError:
      return False
    titm_rank_channel = await self.client.fetch_channel(self.db['titm']['rank_channel'])
    rank_message = await titm_rank_channel.fetch_message(self.db['titm']['rank_message'])
    await rank_message.edit(content = self.__rank_to_msg(rank_dict))
    #await self.__update_titm_roles()
    await self.__update_presence()   
    return True

  async def __send_to_log_channel(self, message):
    log_channel = self.client.get_channel(self.db['channels'].get('log')) # Channel where log is sent
    embed = discord.Embed(title=f"New message in {message.channel}", colour=discord.Colour(0x3e038c)) # Embeded mssg
    embed.add_field(name=str(message.created_at).split('.')[0], value=f"{message.content}") # Add content
    embed.set_footer(text="{}".format(message.author)) # Add author to footer
    try:
      await log_channel.send(embed=embed) # Send
    except:
      await log_channel.send("Could not prase message") # Some messages can't be embeded.

  async def __log_message(self, message):
    channel = str(message.channel) # Get channel where message was sent
    user = str(message.author).split('#')[0] # Get username of person messaging
    message_content = str(message.content).replace("\n", "\n  ") # add some indentation for logging purposes
    custom_print(f'{channel} - {user}:\n  {message_content}', log_file='chat.txt') # Add to log
    
  async def __good_bot(self, message): # She is a good bot
    await message.reply('Nyaa! uωu 💖🎀') # reply nyaa!
  
  async def __w_moon(self, message):
    self.neko_folder.download(f"pics/memes/moon.jpeg")
    with open(f"pics/memes/moon.jpeg", 'rb') as pic:
        picture = discord.File(pic)
    await message.reply("At night!\nMoon is just a nap on a catgirl's joirney into the unknown! 🌙🌙🌙", file = picture)
    self.neko_folder.remove(f"pics/memes/moon.jpeg")

  async def __w_lambo(self, message):
    self.neko_folder.download(f"pics/memes/lambo.jpeg")
    with open(f"pics/memes/lambo.jpeg", 'rb') as pic:
        picture = discord.File(pic)
    await message.reply("🏁 Lambos are only for those who HODL! 🏁", file = picture)
    self.neko_folder.remove(f"pics/memes/lambo.jpeg")
    
  async def __w_burn(self, message):
    self.neko_folder.download(f"pics/memes/burn.png")
    with open(f"pics/memes/burn.png", 'rb') as pic:
        picture = discord.File(pic)
    await message.reply("Every transaction burns tokens! 🔥🔥🔥\nWatch the burn LIVE: https://moonscan.com/catgirl:bsc/0x000000000000000000000000000000000000dead", file = picture)
    self.neko_folder.remove(f"pics/memes/burn.png")

  async def __w_10x(self, message):
    self.neko_folder.download(f"pics/memes/10x.jpeg")
    with open(f"pics/memes/10x.jpeg", 'rb') as pic:
        picture = discord.File(pic)
    await message.reply("📈 My chart says soon™️!\nThose who hold long term will be greatly rewarded!", file = picture)
    self.neko_folder.remove(f"pics/memes/10x.jpeg")

  async def __w_pump(self, message):
    self.neko_folder.download(f"pics/memes/pump.png")
    with open(f"pics/memes/pump.png", 'rb') as pic:
        picture = discord.File(pic)
    await message.reply("🏋️‍♀️Catgirl is always pumping!💪", file = picture)
    self.neko_folder.remove(f"pics/memes/pump.png")

  async def __update_daily_task(self, message):
    if message.channel.id != self.db['daily_task']['channel']:
      return False
    try:
      dt_db = self.db['daily_task']
      dt_db['message'] = message.reference.message_id
      self.db['daily_task'] = dt_db
      await message.reply("Daily task updated, nya!")
      return True
    except AttributeError:
      await message.reply("I can't update the daily task because I don't know what message should I use!. Please use this command when replying to a message")
      return False

  async def check_messages(self, message): # Checks strings in messages and generates responses
    allowed_servers = self.db['servers']
    if message.guild.id not in self.db['servers']:
      await message.reply("I am a bot designed to only work in Catgirl Coin's server. I will NOT work on any other server. Please remove me.")
      return False
    if message.channel.id in self.db['channels'].get('ignored'): return False # Ignore channels
    message_content = str(message.content) # Get the message's content
    for val in list(self.prompts.keys()): # Compare message against list of triggers
      if val in message_content.lower(): # If one of the triggers is in the message
        await self.execute(self.prompts[val], message) # Execute command related to trigger
        break # Only do one trigger per message
    await self.__send_to_log_channel(message) # Send message to log channel
    await self.__log_message(message) # log the message here
    return

  async def update_presence(self, server_id = 845738053259100171):
    await self.__update_presence()
  
  async def send_message(self, message: str, in_channel: int): #Sends a message in the given channel
    channel = self.client.get_channel(in_channel)
    await channel.send(message)
