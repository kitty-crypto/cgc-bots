import os
import sys  
from datetime import datetime
from asyncio import sleep
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(f"{parent_directory}/common")
from database import database 

class clock:
  def __init__(self, client):
    self.client = client
    self.db = database('database.db')
  
  def __convert(self, seconds: int) -> str:
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)
    
  async def start(self, channel = 1016031995043774554):
    time = datetime.now()
    #if time.minute != 0:
    #  print(f"sleeping for {self.__convert(3540 - time.minute*60 - time.second)}")
    #  await sleep(3600 - time.minute*60 - time.second)
    #  return
    if time.minute == self.db['ticktock']:
      print(f"sleeping for {self.__convert(60 - int(time.second))}")
      await sleep(60 - int(time.second))
      return
    await self.client.get_channel(channel).send(f"{'%02s:%02d'%(time.hour,time.minute)}:00")
    self.db['ticktock'] = time.minute
    print(f"{'%02s:%02d'%(time.hour,time.minute)}:00")
    return
