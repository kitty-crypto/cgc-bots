import requests
import discord
import json
import sys
import re
import os
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.split(os.path.dirname(current))[0]
sys.path.append(f"{parent_directory}/common")
from logprint import custom_print

class pricebot:
  def __init__(self, client, api, address, network):
    self.url = api
    self.request = {str(network): [address]}
    self.client = client

  async def update_presence(self):
    await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name= self._pricebot__update_price()))
    
  def __update_price(self):
    request_json = json.loads(re.sub(r"[\[\]]", "", requests.post(self.url, json = self.request).text))
    price = request_json["priceUsd"]
    ppb = "1B CGC = ${:.2f}".format(price * 1e9)
    custom_print(f"price updated to {ppb}")
    return ppb