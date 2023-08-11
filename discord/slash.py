import discord
from nemu import WaifuGenerator as waifus
from discord import app_commands
from discord.ext import commands
from nft_lookup import nftLookup
from spawner import spawner
import asyncio
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from database import database
nft_channel = 954121009538170881
spawn_channel = 911445338295001151

TOKEN = os.environ['discord_key_mae']  # Discord token ID for bot
#client = discord.Client(intents=discord.Intents.all())  # Defining Discord Client
db = database("database.db")
main_channel = 845739075835002930
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
nekoSpawn = spawner(bot, spawn_channel)
lookup = nftLookup(bot)

async def check_channel(interaction: discord.Interaction, allowed_channel: int):
  if interaction.channel_id != allowed_channel:
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(content=f"I can only do this in <#{allowed_channel}>!")
    return False
  await interaction.response.defer(ephemeral=False)
  await asyncio.sleep(2)
  return True

@bot.event
async def on_ready():
 print("bot ready")
 try:
  synced = await bot.tree.sync()
  print(f"Synced {len(synced)} command(s)")
 except Exception as e:
  print(e)

@bot.tree.command(name="nft", description="Lookup an NFT by entering its ID!")
@app_commands.describe(target = "ID:")
async def nft(interaction: discord.Interaction, target: int):
  if not await check_channel(interaction, nft_channel):
    return
  message = await lookup.check_message(interaction, target)
  await interaction.followup.send(embed = message)

@bot.tree.command(name="neko", description="Spawn a Neko! =＾ ● ⋏ ● ＾=")
async def neko(interaction: discord.Interaction):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!neko", interaction, 'None')
  await interaction.followup.send(content=message.get("content"), file=message.get("file"))

@bot.tree.command(name="angry", description="You're angy at a neko! ( •̀ω•́ )σ")
@app_commands.describe(target="Target:")
async def angry(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!angry", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="bless", description="Dorime ε(*´･ω･)っ*ﾟ¨ﾟﾟ･*:..☆")
@app_commands.describe(target="Target:")
async def bless(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!bless", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="blush", description="A neko made you blush! (⁄ ⁄•⁄ω⁄•⁄ ⁄)")
@app_commands.describe(target="Target:")
async def blush(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!blush", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="borger", description="I can has cheesborger? (○ ^ω^)_🍔~~♪")
@app_commands.describe(target = "Target:")
async def borger(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!borger", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="curse", description="You curse a neko ◥(ฅº￦ºฅ)◤")
@app_commands.describe(target = "Target:")
async def curse(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!curse", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="drink", description="Give a drink to a neko 🥤_(ﾟ◇ﾟ；)ノﾞ")
@app_commands.describe(target = "Target:")
async def drink(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!drink", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="food", description="Feed a neko 🍲-(-‿- )")
@app_commands.describe(target="Target:")
async def food(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!food", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="gm", description="Say gm to a neko ( ^ω^ )☀️")
@app_commands.describe(target="Target:")
async def gm(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!gm", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="gn", description="Say gn to a neko ( ︶｡︶)🌒")
@app_commands.describe(target="Target:")
async def gn(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!gn", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="happy", description="If you're happy and you know it~ (≧∇≦)/")
@app_commands.describe(target="Target:")
async def happy(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!happy", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="hug", description="Hug a target neko! ⊂(⁀ᗢ⁀)つ" )
@app_commands.describe(target="Target:")
async def hug(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!hug", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="kick", description="Kick the neko! (┛ಠДಠ)┛彡┻━┻")
@app_commands.describe(target="Target:")
async def kick(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!kick", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="kiss", description="chu chu~ (ΦзΦ) ❤️")
@app_commands.describe(target="Target:")
async def kiss(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!kiss", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="pat", description="pat pat pat~ ^.ᆽ.^= ∫")
@app_commands.describe(target="Target:")
async def pat(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!pat", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="present", description="Give a present to a neko! (๑✪ᆺ✪๑)")
@app_commands.describe(target="Target:")
async def present(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!{name}", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="punch", description="Box with a neko! (ง •̀_•́)ง")
@app_commands.describe(target="Target:")
async def punch(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!punch", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="sad", description="You're sowwy with a neko  (つ>﹏<⊂)")
@app_commands.describe(target="Target:")
async def sad(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!sad", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="tickle", description="Tickle fight with a neko! (つ≧▽≦)つ")
@app_commands.describe(target="Target:")
async def tickle(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!tickle", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="yawn", description="You are so boreeeeed! (!! ´◯`)∑")
@app_commands.describe(target="Target:")
async def yawn(interaction: discord.Interaction, target: discord.User = None):
  if not await check_channel(interaction, spawn_channel):
    return
  message = await nekoSpawn.spawnSlash(f"!yawn", interaction, target)
  await interaction.followup.send(content = message.get("content"), file = message.get("file"))

@bot.tree.command(name="generate", description="Generate a Catgirl using Nemusona's Waifu Generator.")
@app_commands.describe(prompts = "Prompts:")
async def generate(interaction: discord.Interaction, prompts: str = ''):
  generator = waifus(prompts)
  if not await check_channel(interaction, spawn_channel):
    return
  result, promptsUsed = await generator.generate_and_download_image()
  msg = "Here is your catgirl" if not promptsUsed else "Here is your catgirl with prompts: "
  await asyncio.sleep(0)
  with open(result, 'rb') as pic:
    picture = discord.File(pic)
  await interaction.followup.send(content=f"{msg} {promptsUsed}. Credits to [Nemusona's Waifu Generator](<https://waifus.nemusona.com>)", file=picture)
  os.remove(result)

bot.run(TOKEN)