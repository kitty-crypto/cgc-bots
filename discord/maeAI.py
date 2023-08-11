import discord
import openai
import romaji
from threading import Timer

class maeAI:
  def __init__(self, client, allowed_channels, allowed_role):
    self.client = client
    self.allowed_channels = allowed_channels
    self.message_history = []
    self.description = """\
      Mae is a cute catgirl AI assistant from 'Catgirl Coin' - an NFT-based cryptocurrency launched in 2021.
      She's smart, bubbly, and always ends sentences with 'nya~'. She loves making cat-related plays on words like 'purrfect!' and 'nyantastic'.
      Her favorite cryptocurrency is 'Catgirl Coin'. Feel free to ask her anything!"""
    self.allowed_role = allowed_role
    self.conversation_clear_interval = 600  # 10 minutes

    self.start_conversation_timer()

  def start_conversation_timer(self):
    self.conversation_timer = Timer(self.conversation_clear_interval, self.clear_conversation_history)
    self.conversation_timer.start()

  def clear_conversation_history(self):
    self.message_history = []

  def process_message(self, message):
    nickname = message.author.nick  # Get the nickname of the sender
    if nickname is None:
      nickname = message.author.name  # Use the username if there's no nickname
    rmj = romaji.romaji()
    nickname = rmj.get_romaji(nickname)

    msg_content = str(message.content).replace(f"<@{self.client.user.id}>", "")
    user_prompt = f"{self.description}\n\n{self.get_conversation_string()}\n{nickname}: {msg_content}\nMae AI:"
    print(f"{user_prompt}\n\n")
    # Generate a response
    response = openai.Completion.create(
      engine='davinci',
      prompt=user_prompt,
      max_tokens=250,
      n=1,
      stop=[":", "\n", "User", f"{nickname}"],
      temperature=0.7,
    )

    response = response.choices[0].text.strip()
    response = response.replace("Mae AI:", "")
    self.store_message_history(nickname, msg_content, response)
    self.restart_conversation_timer()

    #print(f"{self.get_conversation_string()}\n-----------------------\n")
    return response

  def store_message_history(self, username, message, response):
    if len(self.message_history) >= 10:
      self.message_history = self.message_history[2:]  # Remove the oldest message and response pair
    self.message_history.extend([f"{username}: {message}", "Mae AI: " + response])  # Add the new message, username, and response pair

  def restart_conversation_timer(self):
    self.conversation_timer.cancel()
    self.start_conversation_timer()

  def get_conversation_string(self):
    if not self.message_history:
      return ""
    else:
      return "\n".join(self.message_history)

  async def respond(self, message):
    if f"@{str(self.client.user.id)}" not in message.content:
      return False
    channel = self.client.get_channel(message.channel.id)
    if channel.id not in self.allowed_channels:
      return False
    if self.allowed_role not in [role.id for role in message.author.roles]:
      await message.reply("Sorry, only users with the role 'Bot Tester' can utilise MaeAI as I am currently in testing!")
      return False
    if "!clear" in message.content:
      self.clear_conversation_history()
      self.restart_conversation_timer()
      return True
    response = self.process_message(message)
    await message.reply(response)
    return True
